import sublime
import sublime_plugin


class ContextsListener(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):
		if key == "terminus_tag.exists":
			return any(
				view.settings().get("terminus_view.tag") == operand
				for view in view.window().views()
			)

		elif key == "terminus_panel_visible":
			panel = view.window().active_panel()
			visible = panel and "Terminal" in panel
			return (not visible) if bool(operand) == operator else visible
		elif key == "sidebar_visible":
			visible = view.window().is_sidebar_visible()
			return (not visible) if bool(operand) == operator else visible
