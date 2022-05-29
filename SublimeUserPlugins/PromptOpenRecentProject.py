import sublime
import sublime_plugin


class PromptOpenRecentProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command("new_window")
		sublime.set_timeout(
			lambda: sublime.active_window().run_command("prompt_select_workspace"),
			150,
		)
