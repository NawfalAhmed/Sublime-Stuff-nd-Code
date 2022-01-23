# import tkinter as tk

from tkinter import Tk, Label, Button


def configure(window: Tk, title: str, body: str):
	window.title(title)
	_ = window.bind("<Return>", lambda _: window.destroy())

	btn = Button(window, text="OK")
	btn.pack(side="bottom")
	_ = btn.bind("<Button-1>", lambda _: window.destroy())
	Label(window, text=body).pack(anchor="w")
	Label(window, text=" " * 80).pack(side="bottom", anchor="w")


def main():
	window = Tk()
	configure(window, "Title", "Body")
	window.mainloop()


if __name__ == "__main__":
	main()
