import sublime
import sublime_plugin
import re


class ConvertImportStatementCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		selection = self.view.sel()
		change = False
		for region in selection:
			for line in reversed(self.view.lines(region)):
				pattern = "meta.statement.import.python"
				if self.view.score_selector(line.begin(), pattern):
					contents = self.view.substr(line)
					from_pattern = re.compile(r"^(from\s)(.+)(\simport\s)([^\s]+)")
					sub = re.sub(from_pattern, r"\1\4\3\2", contents)
					contents = (
						(contents.replace("import", "from") + " import ")
						if sub == contents
						else sub
					)
					self.view.replace(edit, line, contents)
					change = True
		if change:
			selection = self.view.sel()
			regions = list(selection)
			selection.clear()
			regions = [
				sublime.Region(line.end())
				for region in regions
				for line in self.view.lines(region)
			]
			selection.add_all(regions)
