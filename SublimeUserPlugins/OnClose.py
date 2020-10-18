import sublime
import sublime_plugin
from os.path import split as splitpath, splitext


class SafeCloseCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		window = self.view.window()
		num_groups = window.num_groups()
		if num_groups <= 1:
			if len(window.sheets_in_group(0)) == 0:
				sublime.status_message("Prevented Project Closing")
				return

		# path = self.view.file_name()
		# path = path.split("\\")
		# try:
		# 	i = path.index("SublimeText") + 1
		# 	# if i + 1 == len(path):
		# 	# 	gitstage = 'wsl git add "' + path[-1] + '"'
		# 	# else:
		# 	# 	gitstage = 'wsl git add "/' + '/'.join(path[i:]) + '"'
		# except ValueError:
		# 	window.run_command("close")
		# 	return
		# gitcommit = 'wsl git commit -m "auto_commited @file-close"'
		# window.run_command("exec", {"shell_cmd": gitcommit, "show_panel": False})
		window.run_command("close")
