import sublime
import sublime_plugin

from time import sleep
from subprocess import run
from threading import Thread
from queue import Full, Queue
from contextlib import suppress


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
			name = self.format_queue.get()
			run(f"black -l 85 {name}", shell=True)
			sleep(3)
			sublime.status_message(f"Formatted: {name}")
			self.format_queue.task_done()

	def on_post_save(self):
		if not self.view.settings().get("python_format_on_save"):
			return
		name, _, ext = self.view.file_name().rpartition("/")[-1].rpartition(".")
		if ext == "py":
			if self.format_queue is None:
				self.format_queue = Queue(maxsize=1)
				self.format_thread = Thread(
					target=self.formatter_async,
					name=f"formatter_async_for_{name}",
					daemon=True,
				)
				self.format_thread.start()
			try:
				self.format_queue.put(self.view.file_name(), block=False)
			except Full:
				print("Prevent Unnecessary Formatting")
