import sublime
import sublime_plugin
import re
import textwrap
from threading import Thread
from subprocess import check_output as syscalloutput, CalledProcessError
from os.path import expanduser
# from subprocess import check_call as syscall


def run_async(select, view):

	def fixstr(contents):
		contents = contents.replace("//", "#").replace("res:#", "res://")
		contents = contents.replace("true", "True").replace("false", "False")
		return re.sub(r",(\s*[\)\]\}])", r"\1", contents)

	name = expanduser("~/Sublime/json-format-temp.py")
	style = expanduser("~/Sublime/json-style.txt")
	open(name, 'w').close()  # clear file contents
	indents = []
	with open(name, 'a') as file:
		if not select:
			contents = view.substr(sublime.Region(0, view.size()))
			file.write(fixstr(contents))
		else:
			regions = view.sel()
			for region in regions:
				contents = view.substr(region)
				match = re.match(r"[\s\n]+", contents)
				indents.append(match.group() if match else None)
				file.write(fixstr(contents.lstrip()))
				file.write("\n# end region\n")

	try:
		contents = syscalloutput("yapf " + name + " --style " + style, shell=True)
	except CalledProcessError:
		sublime.status_message(
			"JsonFormatter ran into an error while trying to format :'("
		)
		return
	contents = contents.decode().replace("\r", "").replace("#", "//")
	contents = contents.replace("True", "true").replace("False", "false")
	sublime.set_timeout_async(
		lambda: view.run_command(
			"format_json_step2",
			{"select": select, "contents": contents, "indents": indents}
		)
	)


class FormatJsonCommand(sublime_plugin.WindowCommand):

	def run(self, select=False):
		Thread(target=run_async, args=(select, self.window.active_view())).start()


class FormatJsonStep2Command(sublime_plugin.TextCommand):

	def run(self, edit, select, contents, indents):
		print(indents)
		contents = re.sub(r'("keys": \[.*\],)\s*("command")', r'\1 \2', contents)
		contents = re.sub(r'([^\s])}', r'\1 }', contents)
		if select:
			contents = list(filter(None, contents.split("\n// end region\n")))
			print(contents)
			regions = self.view.sel()
			zipped = zip(reversed(regions), reversed(contents), reversed(indents))
			for region, region_contents, indent in zipped:
				if indent:
					region_contents = textwrap.indent(region_contents, indent)
				self.view.replace(edit, region, region_contents)
		else:
			self.view.replace(edit, sublime.Region(0, self.view.size()), contents)
