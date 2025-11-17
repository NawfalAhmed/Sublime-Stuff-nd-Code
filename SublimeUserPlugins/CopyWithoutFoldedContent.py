import sublime
import sublime_plugin


# class CopyWithoutFoldedContentCommand(sublime_plugin.TextCommand):
class TestingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Get the selected regions
		selections = self.view.sel()
		if not selections:
			# No selection, copy the whole buffer with folded regions replaced
			selections = [sublime.Region(0, self.view.size())]

		result = []

		for region in selections:
			# Collect lines and handle folded regions
			lines = self.view.lines(region)
			last_end = region.a
			content = []

			for line in lines:
				if line.a >= last_end:
					# Get the content of the line
					line_content = self.view.substr(line)

					# Check if the line is folded
					if self.view.is_folded(line):
						# Replace folded line with '...'
						#  if ...wasnt appended in last
						if content and not content[-1].endswith('...'):
							content.append('...')
					else:
						# Add the actual content if not folded
						content.append(line_content)

					last_end = line.b

			# Join the collected content
			result.append('\n'.join(content))

		# Copy result to clipboard
		sublime.set_clipboard('\n'.join(result))
