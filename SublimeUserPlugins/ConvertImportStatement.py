import sublime
import sublime_plugin


class ConvertImportStatementCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		selection = self.view.sel()
		change = False
		for region in selection:
			for line in reversed(self.view.lines(region)):
				pattern = "meta.statement.import.python"
				if self.view.score_selector(line.begin(), pattern):
					contents = self.view.substr(line)
					contents = contents.replace("import", "from") + " import "
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
