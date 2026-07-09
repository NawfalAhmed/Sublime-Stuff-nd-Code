import csv
import requests
import sys
from datetime import datetime, time, timedelta

import humanize


def get_review_time_in_business_hours(
	*, start: datetime, end: datetime, daily_cap=8
) -> float:

	total_hours = 0.0
	one_day = timedelta(days=1)
	current_day = start.date()
	last_day = end.date()

	while current_day <= last_day:
		if current_day.weekday() < 5:
			day_start = datetime.combine(current_day, time.min)
			day_end = datetime.combine(current_day, time.max)

			# Ensure we do not go past the actual start and end times
			interval_start = max(start, day_start)
			interval_end = min(end, day_end)

			if interval_end > interval_start:
				hrs = (interval_end - interval_start).total_seconds() / 3600
				total_hours += min(hrs, daily_cap)

		current_day += one_day

	return round(total_hours, 2)


class GitHubReviewStatsCollector:
	def __init__(self, github_token):
		self.github_token = github_token
		self.api_url = "https://api.github.com/graphql"
		self.headers = {
			"Authorization": f"bearer {github_token}",
			"Content-Type": "application/json",
		}

		with open(f"review_stats.csv", "w") as f:
			writer = csv.writer(f)
			writer.writerow(
				[
					"Repository",
					"PR #",
					"No. of Review Comments",
					"Review Time (hrs)",
					"Opened At",
					"Merged At",
					"First Review At",
					"Last Review At",
				]
			)

	def run_graphql_query(self, query, variables=None):
		"""Execute a GitHub GraphQL query with pagination support."""
		response = requests.post(
			self.api_url,
			headers=self.headers,
			json={"query": query, "variables": variables},
		)
		response.raise_for_status()
		return response.json()

	def get_pr_review_data(self, owner, repo, cutoff_date, cursor=None):
		"""Get PR review data using a single GraphQL query with pagination support."""
		variables = {
			"owner": owner,
			"repo": repo,
			"prCount": 100,
			"reviewCount": 100,
			"cursor": cursor,
		}

		query = """
		query($owner: String!, $repo: String!, $prCount: Int!, $reviewCount: Int!, $cursor: String) {
			repository(owner: $owner, name: $repo) {
				pullRequests(
					first: $prCount,
					after: $cursor,
					states: [MERGED],
					orderBy: {field: CREATED_AT, direction: DESC}
				) {
					nodes {
						number
						title
						createdAt
						mergedAt
						author {
							login
						}
						reviews(first: $reviewCount) {
							totalCount
							nodes {
								submittedAt
								author {
									login
								}
								comments {
									totalCount
								}
							}
						}
					}
					pageInfo {
						hasNextPage
						endCursor
					}
				}
			}
		}
		"""

		result = self.run_graphql_query(query, variables)

		if "errors" in result:
			print(f"GraphQL Error: {result['errors']}")
			return [], None

		if "data" not in result:
			print(f"Unexpected response format: {result}")
			return [], None

		if result["data"]["repository"] is None:
			print(f"Repository {owner}/{repo} not found or you don't have access")
			return [], None

		pull_requests = result["data"]["repository"]["pullRequests"]
		prs = pull_requests["nodes"]
		page_info = pull_requests["pageInfo"]

		return prs, page_info

	def get_all_pr_review_data(self, owner, repo, cutoff_date):
		"""Get all PR review data with pagination, stopping when we reach the cutoff date."""
		all_prs = []
		has_next_page = True
		cursor = None
		should_continue = True

		while has_next_page and should_continue:
			prs, page_info = self.get_pr_review_data(
				owner, repo, cutoff_date, cursor
			)

			cutoff_reached = False
			filtered_prs = []

			for pr in prs:
				if not pr["createdAt"]:
					continue

				pr_date = datetime.fromisoformat(pr["createdAt"].replace("Z", ""))
				if pr_date < cutoff_date:
					cutoff_reached = True
					should_continue = False
					break

				if repo == "customer-twou" and pr["author"]["login"] != "NawfalAhmed":
					# print(pr["author"]["login"])
					continue
				else:
					if repo !="customer-twou":
						print(pr["author"]["login"])
					filtered_prs.append(pr)

			all_prs.extend(filtered_prs)

			if cutoff_reached or not page_info:
				break

			has_next_page = page_info["hasNextPage"]
			cursor = page_info["endCursor"] if has_next_page else None

			if has_next_page and should_continue:
				print(
					f"Fetched {len(filtered_prs)}  PRs, last PR created at {filtered_prs[-1]['createdAt']}, continuing to next page..."
				)

		return all_prs

	def process_repository(self, repo_slug, cutoff_date):
		if "/" in repo_slug:
			owner, repo = repo_slug.split("/")
		else:
			print(f"Invalid repo format: {repo_slug}. Use 'owner/repo' format.")
			return 0

		print(f"Fetching PRs for {repo} since {cutoff_date}...")
		prs = self.get_all_pr_review_data(owner, repo, cutoff_date)
		print(f"Found {len(prs)} merged PRs for {repo}")

		rows = []
		for pr in prs:
			pr_number = pr["number"]
			opened_at = pr["createdAt"]
			review_times = [
				r["submittedAt"] for r in pr["reviews"]["nodes"] if r["submittedAt"]
			]

			first_review_at = "N/A"
			last_review_at = "N/A"
			review_time_in_hrs = 1

			if review_times:
				first_review_at = min(review_times)
				last_review_at = max(review_times)

				review_time_in_hrs = get_review_time_in_business_hours(
					start=datetime.fromisoformat(opened_at.replace("Z", "")),
					end=datetime.fromisoformat(first_review_at.replace("Z", "")),
					daily_cap=24,
				)

			review_comment_count = sum(
				r.get("comments", {}).get("totalCount", 0)
				for r in pr["reviews"]["nodes"]
			)
			merged_at = pr.get("mergedAt", opened_at)

			# Convert ISO8601 to "YYYY-MM-DD HH:MM:SS" for Google Sheets compatibility
			def fmt(dt):
				if not dt or dt == "N/A":
					return "N/A"
				return datetime.fromisoformat(dt.replace("Z", "")).strftime(
					"%Y-%m-%d %H:%M:%S"
				)

			rows.append(
				(
					repo,
					pr_number,
					review_comment_count,
					review_time_in_hrs,
					fmt(opened_at),
					fmt(merged_at),
					fmt(first_review_at),
					fmt(last_review_at),
				)
			)

		with open(f"review_stats.csv", "a") as f:
			writer = csv.writer(f)
			writer.writerows(rows)

		return len(prs)


def main():
	github_token = sys.argv[1]
	repo_inputs = sys.argv[2].split(",")

	try:
		cutoff_date = datetime(2025, 7, 1)
		if len(sys.argv) > 3:
			cutoff_date = datetime.fromisoformat(sys.argv[3].replace("Z", ""))
	except ValueError:
		print("Invalid date format. Using default cutoff date of 2025-04-01.")

	collector = GitHubReviewStatsCollector(github_token)
	total_prs = 0

	for repo_input in repo_inputs:
		total_prs += collector.process_repository(repo_input, cutoff_date)

	print(
		f"Data collection completed for {len(repo_inputs)} repositories with a total of {total_prs} merged PRs since {cutoff_date}."
	)


if __name__ == "__main__":
	main()
