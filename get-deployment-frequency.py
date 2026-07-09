import csv
import math
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

import matplotlib.pyplot as plt
import requests


def fetch_deploys_for_netlify(auth_token, site_id):
	"""Fetch deploys from Netlify API."""
	base_url = "https://api.netlify.com/api/v1"
	deploy_endpoint = f"/sites/{site_id}/deploys"
	headers = {"Authorization": f"Bearer {auth_token}"}

	print("Fetching deploys from Netlify...")
	response = requests.get(base_url + deploy_endpoint, headers=headers)
	response.raise_for_status()
	return response.json()


commit_refs = [
]

def parse_deploy_dates_for_netlify(deploys, cutoff_date):
	"""Extract and format deploy dates, ignoring data before the cutoff date."""
	published_deploy_dates = []
	total_published = 0

	if not deploys:
		print("No deploys found.")
	else:
		for deploy in deploys:
			published_at = deploy.get("published_at")
			if published_at:
				published_time = datetime.fromisoformat(
					published_at.replace("Z", "+00:00")
				)
				if published_time >= cutoff_date and deploy["commit_ref"] in commit_refs:
					total_published += 1
					published_deploy_dates.append(
						published_time.strftime("%Y-%m-%d")
					)

	return list(reversed(published_deploy_dates)), total_published


def fetch_and_parse_deploys_for_gocd_pipeline(
	gocd_token,
	gocd_domain,
	pipeline_name,
	cutoff_date,
	deploy_stage,
):
	"""Fetch deploys from GoCD API."""
	headers = {
		"Authorization": f"Bearer {gocd_token}",
		"Accept": "application/vnd.go.cd.v1+json",
	}
	after = None
	published_deploy_dates = []
	total_published = 0

	while True:
		after_text = f"after: {after}" if after else ""
		print(f"Fetching deploys for GOCD pipeline '{pipeline_name}'{after_text}...")
		url = f"https://{gocd_domain}/go/api/pipelines/{pipeline_name}/history?page_size=100"
		if after:
			url += f"&after={after}"

		response = requests.get(url, headers=headers)
		response.raise_for_status()
		data = response.json()
		pipelines = data.get("pipelines", [])
		next_href = data.get("_links", {}).get("next", {}).get("href", None)
		if next_href:
			after = parse_qs(urlparse(next_href).query).get("after", [])[0]

		if not pipelines:
			break

		for pipeline in pipelines:
			stage = next(
				(
					stage
					for stage in pipeline["stages"]
					if stage["name"] == deploy_stage
				),
				{},
			)
			if stage.get("status") == "Passed":
				deploy_time = datetime.fromtimestamp(
					pipeline["scheduled_date"] / 1000, tz=timezone.utc
				)
				if deploy_time < cutoff_date:
					return published_deploy_dates, total_published

				total_published += 1
				published_deploy_dates.append(deploy_time.strftime("%Y-%m-%d"))

		if not after:
			break

	return published_deploy_dates, total_published


def save_deploy_dates_to_file(
	pipeline_name, deploy_dates, mode="a", filename="deploy-frequency.csv"
):
	"""Save deploy dates to a file."""
	with open(filename, mode) as file:
		writer = csv.writer(file)
		if mode == "w":
			writer.writerow(["Pipeline", "Deploy Date", "Month in Quarter"])
		repository = pipeline_name.removeprefix("prod-").removesuffix("-prod")
		writer.writerows(
			(repository, deploy_date, get_month_in_quarter(deploy_date))
			for deploy_date in deploy_dates
		)
	print(f"Deploy dates saved to {filename}")


def get_quarter(date):
	"""Convert a date into its corresponding quarter."""
	month = datetime.strptime(date, "%Y-%m-%d").month
	quarter = (month - 1) // 3 + 1
	return f"Q{quarter}"


def count_deploys_by_quarter(deploy_dates):
	"""Count deploys per quarter."""
	return dict(sorted(Counter(get_quarter(date) for date in deploy_dates).items()))


def calculate_weekly_average(quarter_counts):
	"""Calculate weekly average deployments per quarter."""

	def get_quarter_start_end(quarter_str):
		year = datetime.now(tz=timezone.utc).year
		quarter = int(quarter_str[1])
		start_month = 3 * (quarter - 1) + 1
		end_month = start_month + 2
		start = datetime(year, start_month, 1, tzinfo=timezone.utc)
		end = datetime(year, end_month + 1, 1, tzinfo=timezone.utc) - timedelta(
			days=1
		)
		return start, end

	weeks_per_quarter = {}
	now = datetime.now(tz=timezone.utc)
	for quarter in quarter_counts:
		start, end = get_quarter_start_end(quarter)
		if now < end:
			end = now
		weeks = max(1, math.ceil((end - start).days / 7))
		weeks_per_quarter[quarter] = weeks

	weekly_averages = {}

	for quarter, count in quarter_counts.items():
		weekly_averages[quarter] = round(count / weeks_per_quarter[quarter], 2)

	return weekly_averages


def get_month_in_quarter(date):
	"""Convert a date into a month with quarter representation."""
	quarter = get_quarter(date)
	return f"{datetime.strptime(date, '%Y-%m-%d').strftime('%b %Y')} ({quarter})"


def count_deploys_by_month(deploy_dates):
	"""Count deploys per month."""
	return Counter(get_month_in_quarter(date) for date in deploy_dates)


def generate_graph(deploy_dates, output_file="deploy-history-graph.png"):
	"""Generate and save a bar graph for deploy counts."""
	month_counts = count_deploys_by_month(deploy_dates)

	months = list(month_counts.keys())
	counts = [month_counts[month] for month in months]

	plt.figure(figsize=(4.5, 6))
	plt.bar(months, counts, color=(80 / 255, 134 / 255, 236 / 255), width=0.75)
	plt.ylabel("Number of Production Deployments")
	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.savefig(output_file)
	print(f"Graph saved as {output_file}")


def main():
	netlify_token = sys.argv[1]
	netlify_site_id = sys.argv[2]
	gocd_token = sys.argv[3]
	gocd_domain = sys.argv[4]
	gocd_pipelines = [
		pipeline_info.split("/") for pipeline_info in sys.argv[5].split(",")
	]
	try:
		cutoff_date = datetime(2025, 7, 1, tzinfo=timezone.utc)
		if len(sys.argv) > 6:
			input_date = sys.argv[6].replace("Z", "+00:00")
			cutoff_date = datetime.fromisoformat(input_date)
			if cutoff_date.tzinfo is None:
				cutoff_date = cutoff_date.replace(tzinfo=timezone.utc)
	except ValueError:
		print("Invalid date format. Using default cutoff date of 2025-07-01.")
		cutoff_date = datetime(2025, 7, 1, tzinfo=timezone.utc)

	deploy_dates = []
	netlify_deploys = fetch_deploys_for_netlify(netlify_token, netlify_site_id)
	deploy_dates, total_for_netlify = parse_deploy_dates_for_netlify(
		netlify_deploys, cutoff_date
	)

	save_deploy_dates_to_file("customer-twou", deploy_dates, "w")

	count_for_gocd_pipelines = []
	for pipeline_name, deploy_stage in gocd_pipelines:
		pipeline_deploy_dates, total_for_pipeline = (
			fetch_and_parse_deploys_for_gocd_pipeline(
				gocd_token, gocd_domain, pipeline_name, cutoff_date, deploy_stage
			)
		)

		count_for_gocd_pipelines.append((pipeline_name, total_for_pipeline))
		deploy_dates.extend(pipeline_deploy_dates)
		save_deploy_dates_to_file(pipeline_name, pipeline_deploy_dates)

	total_for_gocd = sum(total for _, total in count_for_gocd_pipelines)

	generate_graph(deploy_dates)

	print(f"Total deploys from Netlify Site: {total_for_netlify}")
	print(f"Total deploys from GoCD: {total_for_gocd}")
	for pipeline_name, total in count_for_gocd_pipelines:
		print(f"Total deploys for GoCD pipeline '{pipeline_name}': {total}")
	print(f"Total deploys: {total_for_netlify + total_for_gocd}")

	quarter_counts = count_deploys_by_quarter(deploy_dates)
	weekly_averages = calculate_weekly_average(quarter_counts)

	for quarter in quarter_counts:
		print(
			f"{quarter}: {quarter_counts[quarter]} deploys, "
			f"Weekly Average: {weekly_averages[quarter]}"
		)


if __name__ == "__main__":
	main()
