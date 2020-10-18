import sublime
import sublime_plugin


class OpenKeyBindingsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		file_path = "C:\\Users\\Ibraheem\\Desktop\\SublimeText\\SublimeUserSettings\\Default (Windows).sublime-keymap"
		self.view.window().open_file(file_path)
