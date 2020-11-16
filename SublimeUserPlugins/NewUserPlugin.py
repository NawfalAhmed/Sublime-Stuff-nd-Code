import sublime
import sublime_plugin


class NameInputHandler(sublime_plugin.TextInputHandler):

	def initial_text(self):
		ext = '.py'
		return ext


class NewUserPluginCommand(sublime_plugin.WindowCommand):

	def run(self, name):
		new_file = (
			"C:/Users/Ibraheem/Desktop/SublimeText/SublimeUserPlugins/" + name
		)
		view = self.window.open_file(new_file)
		view.set_scratch(True)
		view.run_command(
			"set_file_type", {"syntax": "Packages/Python/Python.sublime-syntax"}
		)
		sublime.set_timeout(
			lambda: view.run_command(
				"insert_snippet",
				{"name": "Packages/User/Snippets/NewPlugin.sublime-snippet"},
			), 150
		)
		sublime.set_timeout_async(lambda: view.set_scratch(False), 60000)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler()
		else:
			return None
