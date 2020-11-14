import sublime
import sublime_plugin


class UserLogCommand(sublime_plugin.WindowCommand):

	def run(self, type="commands", until=10):
		until *= 1000
		if type == "commands":
			sublime.log_commands(True)
			sublime.set_timeout_async(lambda: sublime.log_commands(False), until)
		elif type == "input":
			sublime.log_input(True)
			sublime.set_timeout_async(lambda: sublime.log_input(False), until)
		else:
			return
