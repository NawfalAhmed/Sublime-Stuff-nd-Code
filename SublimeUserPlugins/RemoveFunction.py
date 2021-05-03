import sublime
import sublime_plugin


class RemoveFunctionCommand(sublime_plugin.TextCommand):

	def run(self, edit, copy=False):
		regions = list(self.view.sel())
		self.view.run_command("expand_selection", {"to": "brackets"})
		if regions == list(self.view.sel()):
			return
		selections = [self.view.substr(region) for region in self.view.sel()]
		self.view.run_command("expand_selection", {"to": "brackets"})
		self.view.run_command("expand_selection_to_word")
		for function, parameters in zip(self.view.sel(), selections):
			if copy:
				sublime.set_clipboard(
					self.view.substr(function).replace(parameters, "")[:-2]
				)
			self.view.replace(edit, function, parameters)
