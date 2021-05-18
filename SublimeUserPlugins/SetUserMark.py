import sublime
import sublime_plugin


class SetUserMarkCommand(sublime_plugin.TextCommand):

	def run(self, edit, clear=False):
		if clear:
			self.view.erase_regions("user_mark")
			return
		marks = list(self.view.sel())
		marks.extend(self.view.get_regions("user_mark"))
		self.view.add_regions(
			"user_mark",
			marks,
			scope="comment",
			flags=(
				sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_OUTLINE
				| sublime.DRAW_NO_FILL | sublime.DRAW_EMPTY
			)
		)
