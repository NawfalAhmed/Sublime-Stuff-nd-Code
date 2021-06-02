import sublime
import sublime_plugin


class create_inputfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		inputname = (
			self.view.file_name().split("\\")[-1].split(".")[0] + "-input.txt"
		)

		def on_done(answer):
			if answer == 0:
				cmd = 'type nul > "' + inputname + '"'
				window.run_command("exec", {"shell_cmd": cmd})

		window = self.view.window()
		message = "Yes, Create Input File "  # + inputname + "~"
		window.show_quick_panel(
			[[message, inputname], ["No", "Cancels Input File Creation"]], on_done
		)
		# window.show_input_panel("Text to Insert:", "Hello, World!",
		#                          on_done, on_change, on_cancel)
