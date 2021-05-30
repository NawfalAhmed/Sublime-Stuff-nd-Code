import sublime
import sublime_plugin
import os
import shutil


class ToggleTypeCheckCommand(sublime_plugin.WindowCommand):

	def run(self):
		path = "$packages/User/LSP-pyright.sublime-settings"
		path = sublime.expand_variables(path, self.window.extract_variables())
		temp = path + ".temp"
		backup = path + ".backup"
		if os.path.exists(backup):
			os.rename(path, temp)
			os.rename(backup, path)
			os.rename(temp, backup)
			sublime.status_message("LSP-pyright: Toggled TypeChecking")
		else:
			shutil.copyfile(path, backup)
			settings_ = sublime.load_settings("LSP-pyright.sublime-settings")
			settings = settings_.get("settings")
			settings['python.analysis.diagnosticSeverityOverrides'].clear()
			settings['python.analysis.typeCheckingMode'] = 'off'
			settings_.set("settings", settings)
			sublime.save_settings("LSP-pyright.sublime-settings")
			sublime.status_message("LSP-pyright: Disabled TypeChecking")
