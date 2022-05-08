import sublime
import sublime_plugin


class AutoRevealCommand(sublime_plugin.EventListener):
	flag = 1
	reset_rate = 15

	def reset_sidebar_expansion(self, window):
		flag = not bool(self.flag % self.reset_rate)
		if flag:
			proj = window.project_data()
			proj["sidebar_reset_flag"] = self.flag // self.reset_rate
			window.set_project_data(proj)

		self.flag += 1
		return flag

	def on_activated(self, view):

		if view.window().is_sidebar_visible():
			if view.settings().get("auto_sidebar_reveal", True):
				window = view.window()
				if self.reset_sidebar_expansion(window):
					sublime.status_message("resetted sidebar")
					sublime.set_timeout(
						lambda: window.run_command("reveal_in_side_bar"), 200
					)
				else:
					window.run_command("reveal_in_side_bar")
