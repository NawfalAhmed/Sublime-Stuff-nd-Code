import sublime
import sublime_plugin


class NameInputHandler(sublime_plugin.TextInputHandler):

	def __init__(self, view):
		self.view = view

	def initial_text(self):
		# syntax = self.view.settings().get("syntax").lower()
		# formats =	[
		# 				["plain", "c++", "sql", "python", "assembly"],
		# 				[".txt", ".cpp", ".sql", ".py", ".asm"]
		# 			]
		# ext = "Buffer.txt"
		ext = '.' + self.view.file_name().split('.')[-1]
		# for i in range(len(formats[0])):
		# 	if formats[0][i] in syntax:
		# 		ext = formats[1][i]
		# 		break
		return ext


class SmoothNewCommand(sublime_plugin.TextCommand):

	def run(self, edit, name):
		view = self.view
		window = view.window()
		window.run_command(
			"exec", {
				"shell_cmd": "subl " + name + " && subl",
				"show_panel": False
				}
			)

	def input(self, args):
		if "name" not in args:
			return NameInputHandler(self.view)
		else:
			return None
