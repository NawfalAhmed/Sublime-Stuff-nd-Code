import sublime
import sublime_plugin
from os.path import split as splitpath


class FormatPythonOnSave(sublime_plugin.ViewEventListener):

	def on_pre_save(self):
		self.view.run_command("lsp_format_document")
		text = self.view.file_name() + " (" + self.view.encoding() + ")"
		# sublime.status_message("Formated and Saved " + text)
		sublime.set_timeout_async(
			lambda: sublime.status_message("Formated and Saved " + text), 100
		)
		# window = self.view.window()

		# def fixformatchanges():
		# 	window.run_command("save")
		# 	s.set("always_prompt_for_file_reload", True)

		# s = self.view.settings()
		# if s.get('format_on_save'):
		# 	s.set("always_prompt_for_file_reload", False)
		# 	s.set('format_on_save', False)

		# 	_, name = splitpath(self.view.file_name())
		# 	command = "yapf \"" + name + "\" --in-place"
		# 	self.view.window().run_command(
		# 		"exec", {
		# 			"shell_cmd": command,
		# 			"show_panel": False
		# 		}
		# 	)
		# 	sublime.set_timeout_async(lambda: fixformatchanges(), 1300)

		# 	sublime.set_timeout_async(lambda: s.set('format_on_save', True), 1500)


class IndentWithTabsOnSave(sublime_plugin.ViewEventListener):

	def on_pre_save(self):
		# if not self.view.settings().get('format_on_save'):
		if self.view.settings().get('indent_with_tabs_on_save'):
			self.view.window().run_command(
				'unexpand_tabs', {"set_translate_tabs": True}
			)
