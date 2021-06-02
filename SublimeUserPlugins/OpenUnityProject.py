import sublime
import sublime_plugin

from glob import glob
from os.path import isdir, split as splitpath


class OpenUnityProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		path = "C:\\Users\\Ibraheem\\Desktop\\Unity Projects"
		pathlen = len(path) + 1
		files = [file[pathlen:] for file in glob(path + "\\*") if isdir(file)]

		def on_done(index):
			if index != -1:
				command = (
					'"' + path + '\\LaunchUnityProject.bat" "' + files[index] + '"'
				)
				self.view.window().run_command(
					"exec", {"shell_cmd": command, "show_panel": True}
				)

		self.view.window().show_quick_panel(files, on_done)
