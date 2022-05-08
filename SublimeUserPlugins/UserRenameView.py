import sublime
import sublime_plugin
from os import path


class TitleInputHandler(sublime_plugin.TextInputHandler):
	def __init__(self, named):
		self.named = named

	def initial_text(self):
		return self.named


class UserRenameViewCommand(sublime_plugin.TextCommand):
	def run(self, edit, title):
		self.view.set_name(title)

	def input(self, args):
		if "title" not in args:
			if self.view.file_name():
				return
			named = self.view.name() or ""
			return TitleInputHandler(named)
