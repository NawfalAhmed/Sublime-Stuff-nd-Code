import sublime
import sublime_plugin
import os
import shutil
from glob import iglob


class UserMoveFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		first = True

		def getdirlist(path):
			path_len = len(path)
			directorylist = [p[path_len + 1 : -1] for p in iglob(path + "/*/")]
			directorylist.insert(0, "..")
			nonlocal first
			if first:
				first = False
			else:
				directorylist.insert(1, "*Move Here*")

			return directorylist

		view = self.view
		src = view.file_name()
		path, dest = os.path.split(src)
		dirlist = getdirlist(path)

		def on_done(index):
			if index != -1:
				nonlocal path
				nonlocal src
				nonlocal dest
				nonlocal dirlist
				if index == 0:
					path, _ = os.path.split(path)
					dirlist = getdirlist(path)
					view.window().show_quick_panel(dirlist, on_done)
				elif index == 1:
					dest = path + "/" + dest
					shutil.move(src, dest)
					src = src.replace("/home/penguin98k", "~")
					dest = dest.replace("/home/penguin98k", "~")
					sublime.status_message(f"moved from {src} to {dest}")
				else:
					path += "/" + dirlist[index]
					dirlist = getdirlist(path)
					view.window().show_quick_panel(dirlist, on_done)

		view.window().show_quick_panel(dirlist, on_done)
