import sublime
import sublime_plugin


class MoveTabBackCommand(sublime_plugin.WindowCommand):

	def run(self):
		view = self.window.active_view()
		group_index, view_index = self.window.get_view_index(view)
		self.window.set_view_index(view, group_index, view_index - 1)
