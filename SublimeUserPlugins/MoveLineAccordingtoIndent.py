import sublime
import sublime_plugin


class SwapUpWithIndentCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.run_command("swap_line_up")
		if self.view.settings().get("fix_indent_on_line_move"):
			self.view.run_command("reindent", {"single_line": True})


class SwapDownWithIndentCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.run_command("swap_line_down")
		if self.view.settings().get("fix_indent_on_line_move"):
			self.view.run_command("reindent", {"single_line": True})


class SwapUpWithIndentAlwaysCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.run_command("swap_line_up")
		self.view.run_command("reindent", {"single_line": True})


class SwapDownWithIndentAlwaysCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.run_command("swap_line_down")
		self.view.run_command("reindent", {"single_line": True})
