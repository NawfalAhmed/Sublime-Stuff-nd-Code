import sublime
import sublime_plugin


class SafeCloseCommand(sublime_plugin.WindowCommand):
	def run(self):
		if self.window.num_groups() <= 1 and not self.window.sheets():
			if self.window.project_file_name():
				self.window.status_message("Prevented Project Closing")
			else:
				self.window.run_command("close")
		else:
			if self.window.sheets_in_group(self.window.active_group()):
				self.window.run_command("close")
			else:
				self.window.run_command("destroy_pane", {"direction": "self"})
				self.window.status_message("Closed Pane")
