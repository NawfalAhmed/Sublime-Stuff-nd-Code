import sublime
import sublime_plugin


class TransposeProCommand(sublime_plugin.TextCommand):

	stored_marks = None

	def run(self, edit):
		selection = self.view.sel()
		regions = list(selection)
		marks = self.view.get_regions("user_mark")
		if marks:
			self.stored_marks = marks
		if self.stored_marks:
			self.view.erase_regions("user_mark")
			selection.add_all(self.stored_marks)
		if all(map(sublime.Region.empty, selection)):
			print("Contained all empty regions")
			self.view.run_command("expand_selection_to_word")
			self.view.run_command("transpose")
		else:
			self.view.run_command("transpose")

		selection.clear()
		selection.add_all(regions)
