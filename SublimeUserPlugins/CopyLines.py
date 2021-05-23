import sublime
import sublime_plugin


class CopyLinesCommand(sublime_plugin.TextCommand):

	def run(self, edit, forward=True):
		for region in self.view.sel():
			line = self.view.line(region)
			line_contents = self.view.substr(line)

			if forward:
				self.view.insert(edit, line.begin(), line_contents + "\n")
			else:
				self.view.insert(edit, line.end(), "\n" + line_contents)

		visible = self.view.lines(self.view.visible_region())
		visible = sublime.Region(visible[0].begin(), visible[-2].end() - 1)
		if not any(map(visible.contains, self.view.sel())):
			self.view.show(self.view.sel()[0], show_surrounds=False, animate=False)
