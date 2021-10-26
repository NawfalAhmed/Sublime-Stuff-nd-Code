import sublime
import sublime_plugin


class TestingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message("Testing Command")
