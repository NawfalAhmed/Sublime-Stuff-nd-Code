import sublime
import sublime_plugin
from itertools import cycle


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
			end = cycle(('end', 'begin'))
			if forward:
				next(end)
			sel.add_all(
				[
					sublime.Region(
						getattr(region, next(end))(), getattr(region, next(end))()
					) for region in regions
				]
			)
