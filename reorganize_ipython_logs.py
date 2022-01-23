#!/usr/bin/env python3.10

import os
from glob import glob
from tkinter import Tk, Label, Button


def removeempty():
	empty = "# IPython log file\n\n\n"
	for i in glob("*log.py.*"):
		with open(i) as file:
			content = file.read()
		if content == empty:
			yield i
			os.remove(i)


def renamelogs(x: str):
	def test():
		for i in list(glob(x)):
			with open(i) as file:
				content = file.read()
			yield (i, len(content))

	# files = sorted(test(), key=lambda x: x[1],reverse=True)
	files = sorted(test())
	newfiles = [f"{x[:-2]}.{(i+1):03}~" for i in range(len(files))]

	for old, new in zip(files, newfiles):
		if old[0] != new:
			yield f"{old[0]} -> {new}"
			os.rename(old[0], new)


def add(window: Tk, name: str, content: list[str]):
	if not content:
		Label(window, text=f"Nothing {name[:-1]}").pack(anchor="w")
	else:
		Label(window, text=name).pack(anchor="w")
		for line in content:
			Label(window, text=line).pack(anchor="w")
		Label(window, text=" " * 40).pack(anchor="w")


def configure(window: Tk):
	window.title("Changes to IpythonLogs")
	_ = window.bind("<Return>", lambda _: window.destroy())

	btn = Button(window, text="OK")
	btn.pack(side="bottom")
	_ = btn.bind("<Button-1>", lambda _: window.destroy())
	Label(window, text=" " * 70).pack(side="bottom", anchor="w")


def main():
	os.chdir("/home/penguin98k/Sublime/IpythonLogs")
	window = Tk()
	configure(window)
	add(window, "Removed:", list(removeempty()))
	add(
		window,
		"Renamed:",
		list(renamelogs("log.py.*")) + list(renamelogs("py39log.py.*")),
	)
	window.mainloop()


if __name__ == "__main__":
	main()
