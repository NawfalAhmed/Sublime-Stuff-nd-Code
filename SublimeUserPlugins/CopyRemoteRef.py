import sublime
import sublime_plugin
import subprocess
import re
import os


def get_file_name_in_pascal(file_path):
	# Extract filename with extension
	filename_with_ext = os.path.basename(file_path.replace("/index", ""))

	# Split the filename and extension
	filename, _ = os.path.splitext(filename_with_ext)

	# Replace hyphens with underscores to handle kebab-case
	filename = filename.replace("-", "_")
	filename = filename.replace(".", "_")

	# Convert to PascalCase if needed
	return (
		filename
		if "_" not in filename
		else "".join(word[0].upper() + word[1:] for word in filename.split("_"))
	)


def get_repo_url(file_path: str):
	"""Get the repository URL from remote"""
	repo_url = subprocess.check_output(
		["git", "remote", "get-url", "origin"],
		universal_newlines=True,
		cwd=file_path,
	).strip()
	repo_url = re.sub(r"git@(ssh\.)?", r"https://", repo_url)
	repo_url = re.sub(r"(https://)[^/]+@", r"\1", repo_url)
	repo_url = re.sub(r"(\.(com|org|io|ca))\:v\d", r"\1", repo_url)
	repo_url = re.sub(r"(\.(com|org|io|ca))\:", r"\1/", repo_url)
	repo_url = re.sub(r"\.git$", r"", repo_url)

	if not repo_url:
		raise Exception(
			f"Remote ({remote}) does not point to a valid repository URL."
		)

	if "github" not in repo_url.lower():
		raise Exception(f"Remote ({remote}) does not point to a GitHub repository.")

	return repo_url


class CopyRemoteRefCommand(sublime_plugin.TextCommand):
	def run(self, edit, link_text=None, fetch_latest=False):
		selection = self.view.sel()
		if len(selection) == 0:
			return
		selected_region = selection[0]

		starting_line = self.view.rowcol(selected_region.begin())[0] + 1
		ending_line = self.view.rowcol(selected_region.end())[0] + 1

		file_path = self.view.file_name()
		file_directory = file_path.rpartition("/")[0]
		repo_root = subprocess.check_output(
			["git", "rev-parse", "--show-toplevel"],
			universal_newlines=True,
			cwd=file_directory,
		).strip()

		if fetch_latest:
			# Fetch the latest changes from origin/master
			subprocess.check_output(["git", "fetch", "origin"], cwd=repo_root)

		# Get the latest commit hash from origin/master or origin/main or origin/2u/main
		try:
			latest_master_commit = subprocess.check_output(
				["git", "rev-parse", "origin/2u/main"],
				universal_newlines=True,
				cwd=repo_root,
			).strip()
		except subprocess.CalledProcessError:
			# If origin/2u/main fails, try origin/master
			try:
				latest_master_commit = subprocess.check_output(
					["git", "rev-parse", "origin/master"],
					universal_newlines=True,
					cwd=repo_root,
				).strip()
			except subprocess.CalledProcessError:
				# If origin/master fails, try origin/main
				try:
					latest_master_commit = subprocess.check_output(
						["git", "rev-parse", "origin/main"],
						universal_newlines=True,
						cwd=repo_root,
					).strip()
				except subprocess.CalledProcessError as e:
					sublime.error_message(f"Failed to get default branch commit: {e}")
					return

		repo_url = get_repo_url(file_directory)
		relative_file_path = file_path.replace(repo_root + "/", "")
		lines = (
			f"L{starting_line}-L{ending_line}"
			if starting_line != ending_line
			else f"L{starting_line}"
		)

		remote_ref = (
			f"{repo_url}/blob/{latest_master_commit}/{relative_file_path}#{lines}"
		)

		ref_of = get_file_name_in_pascal(file_path)

		if link_text == "file_name":
			remote_ref = f"[{ref_of}]({remote_ref})"
		elif link_text == "selection":
			remote_ref = f"[{self.view.substr(selected_region)}]({remote_ref})"

		sublime.set_clipboard(remote_ref)
		sublime.status_message(f"GitHub link copied: {remote_ref}")
