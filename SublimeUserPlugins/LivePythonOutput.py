import sublime
import sublime_plugin


class LivePythonOutputCommand(sublime_plugin.ViewEventListener):

	def on_text_command(self, command_name, args):
		if (command_name, args) != ("insert", {"characters": "\n"}):
			return
		sublime.set_timeout_async(lambda: self.run_async(command_name, args))

	def run_async(self, command_name, args):
		regions = list(self.view.sel())

		if not (
			"python" in self.view.scope_name(regions[0].a) and any(
				view.name() == "Live Output" for view in self.view.window().views()
			)
		):
			return
		self.view.run_command("expand_selection_to_paragraph")
		self.view.run_command("expand_selection_to_indentation")
		selections = self.view.sel()
		full_regions = list(selections)
		selections.clear()
		selections.add_all(regions)
		for region, full_region in zip(regions, full_regions):
			code_block = sublime.Region(full_region.a, (self.view.line(region).b))
			self.view.window().run_command(
				"terminus_send_string",
				{
					"string": self.view.substr(code_block).rstrip(),
					"tag": "LiveIpython",
				}
			)
			self.view.window().run_command(
				"terminus_send_string", {
					"string": "\n",
					"tag": "LiveIpython",
				}
			)
			output_view = next(
				view for view in self.view.window().views()
				if view.name() == "Live Output"
			)
			contents = output_view.substr(sublime.Region(0, output_view.size())
													).split('\n')
			true_output_view = next(
				view for view in self.view.window().views()
				if view.name() == "Live Output Condensed"
			)
			sublime.status_message(
				next(line for line in reversed(contents) if "Out[" in line)
			)
