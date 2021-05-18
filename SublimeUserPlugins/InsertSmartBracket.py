import sublime
import sublime_plugin
import re


class InsertSmartBracketCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		selections = self.view.sel()

		if len(selections) > 1:
			for region in selections:
				self.view.insert(edit, region.end(), ")")
			return

		line = self.view.line(selections[0])
		contents = self.view.substr(line)
		row = self.view.rowcol(selections[0].end())[0]
		match_ = self.view.text_point(row, re.search(r"(\)*)$", contents).start())

		missing = 1
		if selections[0].end() >= match_:
			missing = contents.count('(') - contents.count(')')
			if missing > 1:
				sublime.status_message(f"Added {missing} missing brackets")
			else:
				missing = 1

		self.view.insert(edit, selections[0].end(), ")"*missing)
