import sublime
import sublime_plugin
from time import sleep


class TitleInputHandler(sublime_plugin.TextInputHandler):
	
	def name(self):
		return "title"

	def placeholder(self):
		return "Enter Title"

	def preview(self, value):
		if not value:
			return "Will be set to the Default Title of the Config"


class TerminusOpenWithTitleCommand(sublime_plugin.WindowCommand):
	def run(self, title, **kwargs):
		kwargs["title"] = title
		self.window.run_command("terminus_open", kwargs)

	def input(self, *args, **kwargs):
		return TitleInputHandler()



