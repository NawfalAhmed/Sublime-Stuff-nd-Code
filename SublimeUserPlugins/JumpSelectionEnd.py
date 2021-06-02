import sublime
import sublime_plugin


class JumpSelectionEndCommand(sublime_plugin.TextCommand):
	def run(self, edit, reduce=False, forward=True):
		sel = self.view.sel()
		regions = list(sel)
		sel.clear()
		if reduce:
			if len(regions) == 1:
				jump = sublime.Region(
					regions[-1].end() if forward else regions[0].begin()
				)
			else:
				jump = regions[-1 if forward else 0]
			sel.add(jump)
			self.view.show(jump, show_surrounds=False)
		else:
			sel.add_all(
				[sublime.Region(r.begin(), r.end()) for r in regions]
				if forward
				else [sublime.Region(r.end(), r.begin()) for r in regions]
			)
