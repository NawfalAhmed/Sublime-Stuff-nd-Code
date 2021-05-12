import sublime
import sublime_plugin
from os.path import expandvars

_sublime = expandvars(r"%SublimeInstall%")

files = {
	"Yapf.Style": "C:/Users/Ibraheem/.config/yapf/style",
	"PyCodeStyle": "C:/Users/Ibraheem/.pycodestyle",
	"SublimePlugin": f"{_sublime}/Lib/python38/sublime_plugin.py",
	"Sublime": f"{_sublime}/Lib/python38/sublime.py",
	"SublimePlugin3.3": f"{_sublime}/Lib/python33/sublime_plugin.py",
	"Sublime3.3": f"{_sublime}/Lib/python33/sublime.py"
}


class MenuOpenSpecialFileCommand(sublime_plugin.WindowCommand):

	def run(self):

		panel_items = [[k, v] for k, v in files.items()]
		keys = list(files.keys())

		active_view = self.window.active_view()

		def preview(index):
			if index == -1:
				return
			self.window.open_file(files[keys[index]], sublime.TRANSIENT)

		def on_done(index):
			if index == -1:
				self.window.focus_view(active_view)
				return
			self.window.open_file(files[keys[index]])

		self.window.show_quick_panel(panel_items, on_done, on_highlight=preview)

	# def run(self, file):
	# 	self.window.open_file(value)
	# def input(self, args):
	# 	if "file" not in args:
	# 		return FileInputHandler()


# class FileInputHandler(sublime_plugin.ListInputHandler):

# 	files = {
# 		"Yapf.Style": "C:/Users/Ibraheem/.config/yapf/style",
# 		"PyCodeStyle": "C:/Users/Ibraheem/.pycodestyle"
# 	}

# 	def list_items(self):
# 		files = [(k+" \t "+v,v) for k,v in self.files.items()]
# 		return files

# 	def preview(self, value):
# 		sublime.active_window().open_file(value, sublime.TRANSIENT)

# 	def placeholder(self):
# 		return "Select File To Open"
