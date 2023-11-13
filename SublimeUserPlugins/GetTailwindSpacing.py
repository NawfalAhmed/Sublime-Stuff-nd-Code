import sublime
import sublime_plugin

def map_to_nearest_value(number):
	mapping = {
		0: 0,
		2: 0.5,
		4: 1,
		6: 1.5,
		8: 2,
		10: 2.5,
		12: 3,
		14: 3.5,
		16: 4,
		18: 4.5,
		20: 5,
		24: 6,
		28: 7,
		32: 8,
		36: 9,
		40: 10,
		44: 11,
		48: 12,
		52: 13,
		56: 14,
		60: 15,
		64: 16,
		80: 20,
		96: 24,
		112: 28,
		128: 32,
		144: 36,
		160: 40,
		176: 44,
		192: 48,
		208: 52,
		224: 56,
		240: 60,
		256: 64,
		288: 72,
		320: 80,
		384: 96
	}

	# Find the nearest key that is less than or equal to the given number
	nearest_key = max((k for k in mapping if k <= number), default=None)

	if nearest_key is not None:
		return mapping[nearest_key]
	else:
		# If the number is less than the smallest key in the mapping, return the smallest value
		return mapping[min(mapping.keys())]

class GetTailwindSpacingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				selected_text = self.view.substr(region)
				try:
					number = float(selected_text)
					replacement = str(map_to_nearest_value(number))
					self.view.replace(edit, region, replacement)
					print(replacement)
				except ValueError:
					print('error')
					# Handle non-numeric text if necessary
					pass


38
