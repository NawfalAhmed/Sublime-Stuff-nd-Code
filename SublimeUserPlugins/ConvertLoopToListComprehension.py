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
			"iterator": match.group(2).rstrip(),
		}

		match = re.match(if_pattern, lines[1])
		comprehension = "[{expression} for {items} in {iterator}]\n"
		if match:
			attributes["condition"] = match.group(2).rstrip()
			comprehension = comprehension[:-2] + " if {condition}]\n"

		index = 2 if match else 1
		attributes["expression"] = (
			"(" + "\n".join(lines[index:]) + ")"
			if len(lines) > index + 1
			else lines[-1].strip()
		)
		return comprehension.format(**attributes)

	def run(self, edit):
		loop_pattern = re.compile(r"^\s*for.+in.+:\s*$")

		selection = self.view.sel()
		if len(selection) != 1:
			return

		region = self.view.full_line(selection[0])
		lines = self.view.substr(region).rstrip().split("\n")
		match = re.match(loop_pattern, lines[0])
		if not match:
			return

		selection.clear()
		selection.add(sublime.Region(region.end()))
		self.view.run_command("expand_selection", {"to": "indentation"})
		selection.add(region.cover(selection[0]))

		region = region.cover(selection[0])
		lines = textwrap.dedent(self.view.substr(region).rstrip()).split("\n")

		self.view.replace(edit, region, self.listcomprehension(lines))
