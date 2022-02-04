import sublime
import sublime_plugin
import os
import shutil
from glob import iglob


class UserMoveFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		first = True
		current_first = False

		def getdirlist(path):
			nonlocal first, current_first
			path_len = len(path)
			directorylist = [p[path_len + 1 : -1] for p in iglob(path + "/*/")]
			directorylist.insert(0, "..")
			if first:
				first = False
				current_first = True
			else:
				directorylist.insert(1, "*Move Here*")

			return directorylist

		view = self.view
		src = view.file_name()
		path, dest = os.path.split(src)
		dirlist = getdirlist(path)

		def on_done(index):
			nonlocal current_first
			if index != -1:
				nonlocal path
				nonlocal src
				nonlocal dest
				nonlocal dirlist
				if index == 0:
					path, _ = os.path.split(path)
					dirlist = getdirlist(path)
					view.window().show_quick_panel(dirlist, on_done)
				elif index == 1 and not current_first:
					dest = path + "/" + dest
					shutil.move(src, dest)
					src = src.replace("/home/penguin98k", "~")
					dest = dest.replace("/home/penguin98k", "~")
					sublime.status_message(f"moved from {src} to {dest}")
				else:
					if current_first:
						current_first = False
					path += "/" + dirlist[index]
					dirlist = getdirlist(path)
					view.window().show_quick_panel(dirlist, on_done)

		view.window().show_quick_panel(dirlist, on_done)
