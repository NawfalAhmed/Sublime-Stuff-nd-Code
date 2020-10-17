import sublime
import sublime_plugin
from os.path import split as splitpath, splitext


class RunJupyterCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		def delayedRun():
			self.view.window().run_command(
				"carry_file_to_pane", {"direction": "down"}
				)
			self.view.window().run_command("toggle_zoom_pane", {"fraction": 0.2})
			self.view.window().run_command(
				"terminus_send_string", {
					"string": "jupyter notebook\n",
					"visible_only": True
					}
				)

		self.view.window().run_command(
			"terminus_open", {"cwd": "${file_path:${folder}}"}
			)
		sublime.set_timeout(lambda: delayedRun(), 150)


class RunOnTerminalCommand(sublime_plugin.TextCommand):

	def run(self, edit, terminal="Command Prompt"):

		# def delayedRun():
		# 	self.view.window().run_command(
		# 		"carry_file_to_pane", {"direction": "down"}
		# 		)
		# 	self.view.window().run_command("toggle_zoom_pane", {"fraction": 0.4})
		# 	self.view.window().run_command(
		# 		"terminus_send_string", {
		# 			"string": command,
		# 			"visible_only": True
		# 			}
		# 		)

		_, file_name = splitpath(self.view.file_name())
		base_name, ext = splitext(file_name)
		if ext in (".py", ".c", ".cpp"):
			command = base_name + ext + " -o " + base_name + " && ./\"" + base_name + "\" \n"
			if ext == ".cpp":
				command = "g++ " + command
			elif ext == ".c":
				command = "gcc " + command
			else:
				command = "python \"" + base_name + ext + "\" \n"
		else:
			return
		# print(command)
		self.view.window().run_command(
			"terminus_open", {
				"config_name":
					terminal,
				"title":
					terminal,
				"cwd":
					"${file_path:${folder}}",
				"post_window_hooks":
					[
						("carry_file_to_pane", {
							"direction": "down"
							}), ("toggle_zoom_pane", {
								"fraction": 0.4
								}),
						(
							"terminus_send_string", {
								"string": command,
								"visible_only": True
								}
							)
						]
				}
			)
		# sublime.set_timeout(
		# 	lambda: self.view.window().run_command(
		# 		"terminus_send_string", {
		# 			"string": "rm \"" + name + "\" \n",
		# 			"visible_only": True
		# 			}
		# 		), 150
		# 	)
		# sublime.set_timeout(lambda: delayedRun(), 250)


"""
class RunOnTerminusCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		def delayedRun():
			self.view.window().run_command(
				"carry_file_to_pane", {"direction": "down"}
				)
			self.view.window().run_command("toggle_zoom_pane", {"fraction": 0.4})
			self.view.window().run_command(
				"terminus_send_string", {
					"string": command,
					"visible_only": True
					}
				)

		_, name = splitpath(self.view.file_name())
		command = "py \"" + name + "\" \n"
		self.view.window().run_command(
			"terminus_open", {"cwd": "${file_path:${folder}}"}
			)
		sublime.set_timeout(lambda: delayedRun(), 150)
"""
