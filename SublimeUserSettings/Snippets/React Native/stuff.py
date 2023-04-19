from glob import glob
import re
import os
import tabulate


def rename():
	for name in sorted(glob("*.sublime-snippet")):
		with open(name) as file:
			data = file.read()
			match = re.search(r"description>(.*?)<", data)
			if match:
				os.rename(name, match[1] + ".sublime-snippet")


def table():
	for name in sorted(glob("*.sublime-snippet")):
		with open(name) as file:
			data = file.read()
			match = re.search(r"tabTrigger>(.*?)<", data)
			if match:
				yield (
					match[1],
					name.removesuffix(".sublime-snippet"),
				)


print(tabulate.tabulate(table()))
