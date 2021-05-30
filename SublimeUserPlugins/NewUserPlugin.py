import sublime
import sublime_plugin
import re
import textwrap
from os.path import expanduser


class NameInputHandler(sublime_plugin.TextInputHandler):

	def placeholder(self):
		return "Plugin Name"

	def validate(self, text):
		return bool(re.match(r"^[A-Z][a-zA-Z0-9]+$", text))

	def preview(self, text):
		if text and not re.match(r"^[A-Z][a-zA-Z0-9]*$", text):
			return "Invalid Name, Please Enter Name in PascalCase"


class NewUserPluginCommand(sublime_plugin.WindowCommand):

	def run(self, name):
		sublime.set_timeout_async(lambda: self.run_async(name))

	def run_async(self, name):
		filename = (
			expanduser("~/Sublime/SublimeUserPlugins/") + name
			+ ".py"
		)
		plugin_template = """
			import sublime
			import sublime_plugin


			# class %sCommand(sublime_plugin.${1:Text}Command):
			class TestingCommand(sublime_plugin.${1:Text}Command):
				def run(self${2:, edit}):
					${3:selections = self.view.sel()}

		"""
		plugin_template = textwrap.dedent(plugin_template).lstrip()
		view = self.window.open_file(filename)
		while view.is_loading():
			pass
		if not view.size():
			view.set_scratch(True)
			view.assign_syntax("scope:source.python")

			view.run_command(
				"insert_snippet", {"contents": plugin_template % name}
			)
			sublime.set_timeout_async(lambda: view.set_scratch(False), 60000)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler()
