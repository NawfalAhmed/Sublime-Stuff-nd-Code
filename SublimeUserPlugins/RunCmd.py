import sublime
import sublime_plugin


class RunCmdCommand(sublime_plugin.WindowCommand):
	def run(self, cmd,show_panel=True):
		cmd = cmd.split()
		realcmd = ""
		for value in cmd:
			newvalue = sublime.expand_variables(value, self.window.extract_variables())
			if value != newvalue:
				newvalue = "\""+newvalue+"\""
			realcmd += newvalue + " "
		# realcmd = [ for value in cmd]
		# realcmd = " ".join(realcmd)
		self.window.run_command("exec", {"shell_cmd": realcmd ,"show_panel": show_panel} )
		# self.window.run_command("hide_panel" )
