import sublime
import sublime_plugin

import inspect
from sublime_plugin import application_command_classes
from sublime_plugin import window_command_classes
from sublime_plugin import text_command_classes

from operator import attrgetter
from itertools import groupby


class UserTestCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.view = self.window.new_file()
		self.view.set_scratch(True)
		self.view.set_name("Command List")
		self.view.assign_syntax("scope:source.python")
		self.list_category("Application Commands", application_command_classes)
		self.list_category("Window Commands", window_command_classes)
		self.list_category("Text Commands", text_command_classes)

	def append(self, line):
		self.view.run_command("append", {"characters": line + "\n"})

	def list_category(self, title, command_list):
		self.append("class " + title + ":")
		command_list.sort(key=attrgetter("__module__"))
		for module, module_commands in groupby(
			# command_list, lambda key: key.__module__
			command_list,
			lambda key: key.__module__.split(".")[0],
		):
			module = module.replace(" ", "").replace("-", "")
			module_commands = list(module_commands)
			# if len(module_commands) !=1:
			self.append("\tclass " + module + ":")
			for command in module_commands:
				self.append(f"\t\t{self.get_signature(command)}")
			# else:
			# 	command = module_commands[0]
			# 	self.append(
			# 		"\tclass {}:\t{}".format(module, self.get_signature(command))
			# 	)

		self.append("")

	def get_signature(self, cls):
		clsname = cls.__name__
		name = clsname[0].lower()
		last_upper = False
		for c in clsname[1:]:
			name += ("_" + c.lower()) if (c.isupper() and not last_upper) else (c)
			last_upper = c.isupper()
		if name.endswith("_command"):
			name = name[0:-8]

		args = str(inspect.signature(cls.run))
		return name + "(" + (args[7:] if args[5:7] == ", " else args[5:])
