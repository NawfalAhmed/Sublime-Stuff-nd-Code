import sublime
import sublime_plugin
import re
import textwrap


class ConvertLoopToListComprehensionCommand(sublime_plugin.TextCommand):

	def listcomprehension(self, lines):
		for_pattern = re.compile(r"^for\s+(.+)\s+in\s+(.+)(?=:\s*)")
		if_pattern = re.compile(r"^(\s+)if\s+(.+)(?=:\s*)")

		match = re.match(for_pattern, lines[0])
		attributes = {
			"condition": None,
			"expression": None,
			"items": match.group(1),
			"iterator": match.group(2).rstrip()
		}

		match = re.match(if_pattern, lines[1])
		if match:
			attributes["condition"] = match.group(2).rstrip()
			attributes["expression"] = "(" + "\n".join(
				lines[2:]
			) + ")" if len(lines) > 3 else lines[-1].strip()
			comprehension = "[{expression} for {items} in {iterator} if {condition}]\n"
		else:
			attributes["expression"] = "(" + "\n".join(
				lines[1:]
			) + ")" if len(lines) > 2 else lines[-1].strip()
			comprehension = "[{expression} for {items} in {iterator}]\n"

		return comprehension.format(**attributes)

	def run(self, edit):
		loop_pattern = re.compile(r"^\s*for.+in.+:\s*$")

		selection = self.view.sel()
		if len(selection) != 1:
			return

		region = self.view.full_line(selection[0])
		lines = self.view.substr(region).rstrip().split('\n')
		match = re.match(loop_pattern, lines[0])
		if not match:
			return

		selection.clear()
		selection.add(sublime.Region(region.end()))
		self.view.run_command("expand_selection", {"to": "indentation"})
		selection.add(region.cover(selection[0]))

		lines = textwrap.dedent(
			self.view.substr(region.cover(selection[0])).rstrip()
		).split('\n')

		self.view.replace(edit, region, self.listcomprehension(lines))
