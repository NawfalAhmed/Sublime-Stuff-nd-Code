import sublime
import sublime_plugin


class CycleOutputPanelsCommand(sublime_plugin.WindowCommand):

	def run(self):
		exclude_panels = [
			"output.diagnostics", "output.find_results", "output.Linux Terminal",
			"output.Windows Terminal"
		]

		output_panels = [
			name for name in self.window.panels()
			if "output." == name[:7] and name not in exclude_panels
		]
		if output_panels:
			msg = None
			if len(output_panels) == 1:
				msg = "Alert: Only a single Ouput Panel ("
				index = -1
			else:
				try:
					index = output_panels.index(self.window.active_panel())
				except ValueError:
					index = -1

			index = 0 if (index + 1) == 0 else (index+1) % len(output_panels)

			name = output_panels[index][7:]
			name = "Build Results" if "exec" == name else name
			msg = msg + name + ") exists" if msg else "Opened Panel: " + name

			self.window.run_command("show_panel", {"panel": output_panels[index]})
			sublime.status_message(msg)
		else:
			sublime.status_message("Error: No Ouput Panel Exists")
