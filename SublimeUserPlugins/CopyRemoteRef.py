import sublime
import sublime_plugin
import subprocess
import re

def get_repo_url(file_path: str):
	"""Get the repository URL from remote"""
	repo_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], universal_newlines=True, cwd=file_path).strip()
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
	def run(self, edit):
		selection = self.view.sel()
		if len(selection) == 0:
			return
		selected_region = selection[0]

		starting_line = self.view.rowcol(selected_region.begin())[0] + 1
		ending_line = self.view.rowcol(selected_region.end())[0] + 1

		file_path = self.view.file_name()
		file_directory = file_path.rpartition('/')[0]
		repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], universal_newlines=True, cwd=file_directory).strip()

		repo_url = get_repo_url(file_directory)
		relative_file_path = file_path.replace(repo_root + '/', '')
		lines = f"L{starting_line}-L{ending_line}" if starting_line != ending_line else f"L{starting_line}"

		remote_ref = f"{repo_url}/blob/master/{relative_file_path}#{lines}"

		sublime.set_clipboard(remote_ref)
