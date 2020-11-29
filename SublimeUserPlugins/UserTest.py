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
		self.view.run_command(
			"set_file_type", {"syntax": "Packages/Python/Python.sublime-syntax"}
		)
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
			command_list, lambda key: key.__module__.split('.')[0]
		):
			module = module.replace(' ', '').replace('-', '')
			module_commands = list(module_commands)
			# if len(module_commands) !=1:
			self.append("\tclass " + module + ":")
			for command in module_commands:
				self.append(
					"\t\t{cmd}{args}".format(
						cmd=self.get_name(command), args=self.get_args(command.run)
					)
				)
			# else:
			# 	command = module_commands[0]
			# 	self.append(
			# 		"\tclass {mod}:\t{cmd}{args}".format(
			# 			mod = module,
			# 			cmd=self.get_name(command), args=self.get_args(command.run)
			# 		)
			# 	)

		self.append("")

	def get_name(self, cls):
		clsname = cls.__name__
		name = clsname[0].lower()
		last_upper = False
		for c in clsname[1:]:
			if c.isupper() and not last_upper:
				name += '_'
				name += c.lower()
			else:
				name += c
			last_upper = c.isupper()
		if name.endswith("_command"):
			name = name[0:-8]
		return name

	def get_args(self, func):
		args = str(inspect.signature(func))
		return '(' + (args[7:] if args[5:7] == ', ' else args[5:])
