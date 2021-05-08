import sublime
import sublime_plugin


class TransposeProCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		selection = self.view.sel()
		regions = list(selection)
		selection.add_all(self.view.get_regions("mark"))
		if all(map(sublime.Region.empty, selection)):
			print("Contained all empty regions")
			self.view.run_command("expand_selection_to_word")
			self.view.run_command("transpose")
		else:
			self.view.run_command("transpose")

		selection.clear()
		selection.add_all(regions)
