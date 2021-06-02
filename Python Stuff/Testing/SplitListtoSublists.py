from itertools import groupby
from operator import attrgetter

# command_list = [Test1, Test2, Test2, Test3, Test3, Test3, Test1, Test1, Test2]
# command_list = []  #add list of class objects

# for key, keylist in groupby(command_list, attrgetter("__module__")):
# 	print(key, list(keylist))

command_list.sort(key=attrgetter("__module__"))
for module, module_commands in groupby(
	command_list, lambda x: x.__module__.split(".")[0]
):
	print(module, module_commands)
