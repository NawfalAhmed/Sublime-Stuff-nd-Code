# import sublime
import sublime_plugin
from os.path import split as splitpath
from glob import glob


class ZipThisDirectoryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		dirpath, dirname = splitpath(splitpath(view.file_name())[0])
		command = (
			"zip ../{name} -u -9 -r *"
			if not glob(dirpath + "/ZIPS")
			else "zip ../ZIPS/{name} -u -9 -r *"
		)
		prefixes = [
			"BSCS18010_",
			"BSCS18010_Nawfal_",
			"BSCS18010-",
		]
		suffixes = [
			"_BSCS18010",
		]
		styles = []
		styles.append(dirname)
		styles.extend(prefix + dirname for prefix in prefixes)
		styles.extend(dirname + suffix for suffix in suffixes)

		def on_done(index):
			if index != -1:
				self.view.window().run_command(
					"exec",
					{
						"shell_cmd": command.format(name=styles[index]),
						"show_panel": False,
					},
				)

		view.window().show_quick_panel(styles, on_done)
