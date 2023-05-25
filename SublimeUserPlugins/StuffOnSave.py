import os
from string import Template
import sublime
import sublime_plugin

from time import sleep
from subprocess import PIPE, CalledProcessError, run
from threading import Thread
from queue import Full, Queue
from contextlib import suppress

run_args = {"shell": True, "executable": "/usr/local/bin/fish"}
command = {
	"ts": Template("npx prettier --write $name"),
	"py": Template("python -m black -l 85 '$name'"),
}


class StuffOnSave(sublime_plugin.ViewEventListener):
	def __init__(self, *args, **kwargs):
		self.format_queue = None
		self.format_thread = None
		super().__init__(*args, **kwargs)

	def on_pre_save(self):

		if self.view.settings().get("indent_with_tabs_on_save"):
			self.view.window().run_command(
				"unexpand_tabs", {"set_translate_tabs": True}
			)

	def formatter_async(self):
		while True:
			name, type_ = self.format_queue.get()
			dir_name = os.path.dirname(name)
			file_name = os.path.basename(name)
			if type_ == "py":
				output = run(
					command[type_].substitute(name=name) + " --check", **run_args
				)
				if not "unchanged" in str(output):
					print("Formatting")
					run(command[type_].substitute(name=name), **run_args)
					sleep(2)
			elif type_ == "ts":
				print("Formatting")
				try:
					run(
						command[type_].substitute(name=file_name),
						check=True,
						capture_output=True,
						cwd=dir_name,
						**run_args,
					)
					sleep(1)
				except CalledProcessError as e:
					sublime.error_message(e.stderr)

			sublime.status_message(f"Formatted {type_}: {name}")
			self.format_queue.task_done()

	def on_post_save(self):

		name, _, ext = self.view.file_name().rpartition("/")[-1].rpartition(".")
		if ext == "py":
			if not self.view.settings().get("python_format_on_save"):
				return
			if self.format_queue is None:
				self.format_queue = Queue(maxsize=1)
				self.format_thread = Thread(
					target=self.formatter_async,
					name=f"formatter_async_for_{name}",
					daemon=True,
				)
				self.format_thread.start()
			try:
				self.format_queue.put([self.view.file_name(), "py"], block=False)
			except Full:
				print("Prevent Unnecessary Formatting")
		elif ext in ("ts", "tsx", "js", "jsx"):
			if not self.view.settings().get("ts_format_on_save"):
				return
			if self.format_queue is None:
				self.format_queue = Queue(maxsize=1)
				self.format_thread = Thread(
					target=self.formatter_async,
					name=f"formatter_async_for_{name}",
					daemon=True,
				)
				self.format_thread.start()
			try:
				self.format_queue.put([self.view.file_name(), "ts"], block=False)
			except Full:
				print("Prevent Unnecessary Formatting")
