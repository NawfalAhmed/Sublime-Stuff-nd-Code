import sublime
import sublime_plugin


class SetUserMarkCommand(sublime_plugin.TextCommand):
	def run(self, edit, clear=False, convert=False):
		view = self.view
		if convert or clear:
			if convert:
				view.sel().add_all(view.get_regions("user_mark"))
			view.erase_regions("user_mark")
		else:
			view.add_regions(
				"user_mark",
				list(view.sel()) + view.get_regions("user_mark"),
				scope="comment",
				flags=(sublime.DRAW_NO_FILL | sublime.DRAW_EMPTY),
			)
