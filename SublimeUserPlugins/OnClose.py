import sublime
import sublime_plugin


class SafeCloseCommand(sublime_plugin.WindowCommand):

	def run(self):
		if self.window.num_groups() <= 1 and not self.window.sheets_in_group(0):
			sublime.status_message("Prevented Project Closing")
		else:
			self.window.run_command("close")
