import sublime
import sublime_plugin

import textwrap
from threading import Thread
from subprocess import run, CalledProcessError

def run_async(view, file_name: str):
	try:
		path,_,file_name = file_name.rpartition('/')
		# print("filename, path", path, file_name)
		prettier_result = run(
			f"prettier {file_name}",
			shell=True,
			capture_output=True,
			text=True,
			executable="/usr/local/bin/fish",
			cwd=path
		)
		prettier_result.check_returncode()
		sublime.status_message(f"Prettified {file_name}")
	except CalledProcessError:
		annotation = textwrap.dedent(
			"""
				<body>
					<style>
						#annotation-error {
							background-color: color(var(--background) blend(#fff 95%));
						}
						html.dark #annotation-error {
							background-color: color(var(--background) blend(#fff 95%));
						}
						html.light #annotation-error {
							background-color: color(var(--background) blend(#000 85%));
						}
						a {
							text-decoration: inherit;
						}
					</style>
					<div class="error" id=annotation-error>
						<span class="content">
							__content__
						</span>
					</div>
				</body>
			"""
		).lstrip()
		view.add_regions(
			"format_error",
			[sublime.Region(view.line(view.sel()[0]).begin() + 1)],
			scope="invalid",
			annotations=[annotation.replace("__content__", "Invalid Syntax")],
			flags=(sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
			on_close=lambda: (
				view.erase_regions("format_error"),
				view.hide_popup(),
			),
		)
		sublime.status_message(
			"PrettifyJS's dependency 'prettier' ran into an error"
			"while trying to format :'("
		)
		print("Error[PrettifyJS]:",  prettier_result.stderr)
		return

class UserPrettifyJsCommand(sublime_plugin.WindowCommand):
	def run(self):
		file_name = self.window.active_view().file_name()
		# print(file_name)
		if file_name and file_name.rpartition('.')[-1] in ('ts','js','tsx','jsx'):
			Thread(
				target=run_async,
				args=(self.window.active_view(), file_name),
				name="PrettifyJS.run_async",
			).start()
