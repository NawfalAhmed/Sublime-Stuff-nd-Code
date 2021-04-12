import sublime
import sublime_plugin


class DeleteAssemblyStuffCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command(
			"run_cmd", {
				"cmd": "del ${file_base_name}.com & del ${file_base_name}.lst & del ${file_base_name}.obj & del ${file_base_name}.exe"
			}
		)
