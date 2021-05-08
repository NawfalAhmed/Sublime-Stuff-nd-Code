import sublime
import sublime_plugin
from collections import OrderedDict

files = OrderedDict(
	**{
		"Yapf.Style": "C:/Users/Ibraheem/.config/yapf/style",
		"PyCodeStyle": "C:/Users/Ibraheem/.pycodestyle",
		"Sublime": "C:/Program Files/Sublime Text 3/sublime.py",
		"SublimePlugin": "C:/Program Files/Sublime Text 3/sublime_plugin.py",
	}
)
files.move_to_end("Sublime", True)
files.move_to_end("SublimePlugin", True)


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
