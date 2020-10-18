import sublime
import sublime_plugin


class OpenKeyBindingsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		file_path = "Redacted"
		self.view.window().open_file(file_path)
