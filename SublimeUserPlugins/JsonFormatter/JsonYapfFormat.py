import sublime
import sublime_plugin

import subprocess


class JsonYapfFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		content = self.view.substr(sublime.Region(0, self.view.size()))
		content = content.replace("//", "#")
		content = content.replace("res:#", "res://")

		path = sublime.packages_path() + "/JsonFormatter/"
		with open(path + "temporary.notpy", "w") as file:
			file.write(content)
		command = 'yapf "' + path + 'temporary.notpy" -i --style style.txt'
		process = subprocess.Popen(command, shell=True)
		process.wait()
		with open(path + "temporary.notpy", "r") as file:
			content = file.read()
		content = content.replace("#", "//")
		self.view.replace(edit, sublime.Region(0, self.view.size()), content)

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")
