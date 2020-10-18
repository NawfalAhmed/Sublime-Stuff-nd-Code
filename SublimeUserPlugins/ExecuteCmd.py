import sublime
import sublime_plugin


class ExecuteCmdCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window = self.view.window()
		def on_done(cmd):
			cmd = cmd.split()
			realcmd = ""
			for value in cmd:
				newvalue = sublime.expand_variables(value, window.extract_variables())
				if value != newvalue:
					newvalue = "\""+newvalue+"\""
				realcmd += newvalue + " "
			window.run_command("exec", {"shell_cmd": realcmd } )
		def on_change(cmd):
			pass

		def on_cancel():
			pass

		window.show_input_panel("Command:", "start.",
														on_done, on_change, on_cancel)
