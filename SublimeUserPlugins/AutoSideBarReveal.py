import sublime
import sublime_plugin


class AutoRevealCommand(sublime_plugin.EventListener):

	def on_activated(self, view):
		if view.window().is_sidebar_visible():
			if view.settings().get("auto_sidebar_reveal", True):
				view.window().run_command("reveal_in_side_bar")
