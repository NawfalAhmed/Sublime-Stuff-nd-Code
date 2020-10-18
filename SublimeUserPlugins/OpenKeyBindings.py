import sublime
import sublime_plugin


class OpenKeyBindingsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		file_path = sublime.packages_path(
		) + "\\User\\Default (Windows).sublime-keymap"
		self.view.window().open_file(file_path)
