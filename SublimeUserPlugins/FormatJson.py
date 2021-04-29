import sublime
import sublime_plugin
import re
from os import system


class FormatJsonCommand(sublime_plugin.TextCommand):

	def run(self, edit, select=False):
		# self.view.run_command("expand_selection", {"to": "brackets"})
		# self.view.run_command("expand_selection", {"to": "brackets"})
		contents = self.view.substr(sublime.Region(0, self.view.size()))
		# clear file contents
		system(r"break > C:\Users\Ibraheem\Desktop\SublimeText\ffformat.py")
		if select:
			regions = self.view.sel()
			for region in regions:
				region_contents = self.view.substr(region).lstrip()
				self.view.run_command(
					"format_json_step1", {
						"select": select,
						"contents": region_contents,
					}
				)
		else:
			self.view.run_command(
				"format_json_step1", {
					"select": select,
					"contents": contents,
				}
			)
		sublime.set_timeout_async(lambda: self.delayedrun(select), 1500)
		# sublime.set_timeout_async(
		# 	lambda: self.view.
		# 	run_command("reindent", {"single_line": False}, 1500)
		# )

	def delayedrun(self, select):
		self.view.run_command("format_json_step2", {"select": select})

		if not select:
			self.view.window().run_command("save")


class FormatJsonStep1Command(sublime_plugin.TextCommand):

	def run(self, edit, select, contents):

		contents = contents.replace("//", "#")
		contents = contents.replace("res:#", "res://")
		indexes = re.finditer(",\\s*[\\)\\]\\}]", contents)
		indexes = [i.start() for i in indexes]
		contents = "".join(
			[char for i, char in enumerate(contents) if i not in indexes]
		)
		contents = contents.replace("true", "True").replace("false", "False")
		name = "C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformat.py"
		style = "C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ssstyle.txt"
		command = "yapf " + name + " --in-place --style " + style
		self.view.window().run_command(
			"exec", {
				"shell_cmd": command,
				"show_panel": False,
			}
		)
		# with open(path + 'temporary.notpy', 'w') as file:
		with open(name, 'a') as file:
			file.write(contents)
			if select:
				file.write("\n# end region\n")

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")


class FormatJsonStep2Command(sublime_plugin.TextCommand):

	def run(self, edit, select):
		with open(
			"C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformat.py", 'r'
		) as file:
			contents = file.read()
		contents = contents.replace("#", "//")
		contents = contents.replace("True", "true").replace("False", "false")

		# with open(
		# 	"C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformatoutputcontent.sublime-keymap",
		# 	'w'
		# ) as file:
		# 	file.write(contents)
		# 	if select:
		# 		file.write("\n# end region\n")

		startindexes = sorted(
			[i.end() - 1 for i in re.finditer("keys\": \\[.*\\],\n", contents)],
			reverse=True
		)
		endindexes = sorted(
			[
				i.end() - 1
				for i in re.finditer("keys\": \\[.*\\],\n\\s*", contents)
			],
			reverse=True
		)
		contentslist = list(contents)
		for s, e in zip(startindexes, endindexes):
			contentslist[e] = " "
			del contentslist[s:e]
		contents = "".join(contentslist)
		if select:
			contents = contents.split("\n// end region\n")
			print(contents)
			regions = self.view.sel()
			for region, region_contents in zip(regions, contents):
				self.view.replace(edit, region, region_contents)
		else:
			self.view.replace(edit, sublime.Region(0, self.view.size()), contents)

		# with open(
		# 	"C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformatoutput.sublime-keymap",
		# 	'w'
		# ) as file:
		# 	file.write(contents)
		# 	if select:
		# 		file.write("\n# end region\n")

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")
