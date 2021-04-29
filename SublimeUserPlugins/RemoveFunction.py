import sublime
import sublime_plugin


class RemoveFunctionCommand(sublime_plugin.TextCommand):

	def run(self, edit, copy=False):
		self.view.run_command("expand_selection", {"to": "brackets"})
		selections = [self.view.substr(region) for region in self.view.sel()]
		self.view.run_command("expand_region")
		self.view.run_command("expand_region")
		for region, text in zip(self.view.sel(), selections):
			if copy:
				sublime.set_clipboard(self.view.substr(region).replace(text, "")[:-2])
			self.view.replace(edit, region, text)
