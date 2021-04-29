import sublime
import sublime_plugin

_plugin_template = """
import sublime
import sublime_plugin


class ${1:%s}Command(sublime_plugin.${2:Text}Command):
	def run(self${3:, edit}):
		${4:self.view.insert(edit, 0, "Hello, World!")}

"""


class NameInputHandler(sublime_plugin.TextInputHandler):

	def placeholder(self):
		return "Plugin Name"


class NewUserPluginCommand(sublime_plugin.WindowCommand):

	def run(self, name):
		sublime.set_timeout_async(lambda: self.run_async(name))

	def run_async(self, name):
		filename = (
			"C:/Users/Ibraheem/Desktop/SublimeText/SublimeUserPlugins/" + name
			+ ".py"
		)
		view = self.window.open_file(filename)
		while view.is_loading():
			pass
		if not view.size():
			view.set_scratch(True)
			view.set_syntax_file("Packages/Python/Python.sublime-syntax")

			view.run_command(
				"insert_snippet", {"contents": _plugin_template[1:] % name}
			)
			sublime.set_timeout_async(lambda: view.set_scratch(False), 60000)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler()
