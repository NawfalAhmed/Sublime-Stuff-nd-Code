import sublime
import sublime_plugin

class TerminusViewListener(sublime_plugin.EventListener):

	def on_query_context(self, view, key, operator, operand, match_all):
		if key == "terminus_tag.exists":
			return any(
				view.settings().get("terminus_view.tag") == operand
				for view in view.window().views()
			)
