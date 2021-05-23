import sublime
import sublime_plugin


class InitialEmptyPaneCheckCommand(sublime_plugin.EventListener):

	def on_pre_close(self, view):
		window = view.window()
		if not window:
			return
		group = window.active_group()
		if window.num_groups() > 1:
			if len(window.sheets_in_group(group)) == 1:
				if window.get_view_index(view)[1] != -1:
					sublime.set_timeout_async(
						lambda: window.run_command("final_empty_pane_check"), 100
					)

	def on_post_window_command(self, window, command_name, args):
		if command_name == "carry_file_to_pane":
			sublime.set_timeout_async(
				lambda: window.run_command("final_empty_pane_check"), 100
			)


class FinalEmptyPaneCheckCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		window = self.view.window()
		num_groups = window.num_groups()
		if num_groups <= 1:
			return
		originalgroup = window.active_group()
		groups = [i for i in range(num_groups)]
		groups[0], groups[originalgroup] = originalgroup, 0
		for groupid in groups:
			window.focus_group(groupid)
			if len(window.sheets_in_group(groupid)) == 0:
				sublime.status_message("...Closing Pane...")
				window.run_command("destroy_pane", {"direction": "self"})
				break
		if originalgroup < window.num_groups():
			window.focus_group(originalgroup)
