import sublime
import sublime_plugin
import re


class FormatJsonCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.run_command("format_json_step1")
		sublime.set_timeout_async(lambda: self.delayedrun(), 2000)

	def delayedrun(self):
		self.view.run_command("format_json_step2")
		self.view.window().run_command("save")


class FormatJsonStep1Command(sublime_plugin.TextCommand):

	def run(self, edit):

		content = self.view.substr(sublime.Region(0, self.view.size()))
		content = content.replace("//", "#")
		content = content.replace("res:#", "res://")
		indexes = re.finditer(",\\s*[\\)\\]\\}]", content)
		indexes = [i.start() for i in indexes]
		content = "".join(
			[char for i, char in enumerate(content) if i not in indexes]
		)
		content = content.replace("true", "True").replace("false", "False")
		name = "C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformat.py"
		style = "C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ssstyle.txt"
		command = "yapf " + name + " --in-place --style " + style
		self.view.window().run_command(
			"exec", {
				"shell_cmd": command,
				"show_panel": False
			}
		)
		# with open(path + 'temporary.notpy', 'w') as file:
		with open(name, 'w') as file:
			file.write(content)

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")


class FormatJsonStep2Command(sublime_plugin.TextCommand):

	def run(self, edit):
		with open(
			"C:\\Users\\Ibraheem\\Desktop\\SublimeText\\ffformat.py", 'r'
		) as file:
			content = file.read()
		content = content.replace("#", "//")
		content = content.replace("True", "true").replace("False", "false")

		startindexes = sorted(
			[i.end() - 1 for i in re.finditer("keys\": \\[.*\\],\n", content)],
			reverse=True
		)
		endindexes = sorted(
			[i.end() - 1 for i in re.finditer("keys\": \\[.*\\],\n\\s*", content)],
			reverse=True
		)
		contentlist = list(content)
		for s, e in zip(startindexes, endindexes):
			contentlist[e] = " "
			del contentlist[s:e]
		content = "".join(contentlist)
		self.view.replace(edit, sublime.Region(0, self.view.size()), content)

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")
