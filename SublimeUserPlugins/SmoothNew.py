import sublime
import sublime_plugin


class NameInputHandler(sublime_plugin.TextInputHandler):
	def __init__(self, view):
		self.view = view

	def initial_text(self):
		ext = "." + self.view.file_name().split(".")[-1]
		return ext


class SmoothNewCommand(sublime_plugin.WindowCommand):
	def run(self, name):
		view = self.window.open_file(name)
		view.set_scratch(True)
		sublime.set_timeout(lambda: view.set_scratch(False), 60000)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler(self.window.active_view())


class SmoothNewBufferCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.new_file()
		view.set_scratch(True)
		view.assign_syntax("scope:source.notes")
		sublime.set_timeout(lambda: view.set_scratch(False), 60000)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler(self.window.active_view())
