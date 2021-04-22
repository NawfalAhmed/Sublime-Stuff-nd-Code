import sublime
import sublime_plugin


class SendPythonStringCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		for region in self.view.sel():
			self.view.window().run_command(
				"terminus_send_string", {
					"string": self.view.substr(region),
					"tag": "Ipython",
				}
			)

		self.view.window().run_command(
			"toggle_terminus_panel", {
				"cmd": "ipython",
				"cwd": "${file_path:${folder}}",
				"panel_name": "Ipython",
				"tag": "Ipython"
			}
		)
