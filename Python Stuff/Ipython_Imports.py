from os.path import split as split_path
from random import random as random_
import importlib

__methods = {
	"bisect": ["bisect_left", "bisect_right"],
	"bs4": "BeautifulSoup",
	"collections": "deque",
	"collections.abc": ["Iterable", "Mapping"],
	"concurrent": "futures",
	"concurrent.futures": "Future",
	"contextlib": "suppress",
	"copy": "deepcopy",
	"dataclasses": "dataclass",
	"datetime": "datetime",
	"flask": "Flask",
	"functools": ["partial", "wraps"],
	"glob": "glob",
	"heapq": ["heappop", "heappush"],
	"itertools": [
		"chain",
		"combinations",
		"cycle",
		"groupby",
		"permutations",
		"filterfalse",
	],
	"math": ["ceil", "inf", "sqrt"],
	"os": "system",
	"os.path": ["expandvars", "isdir"],
	"pathlib": "Path",
	"playsound": "playsound",
	"pprint": "pprint",
	"queue": "Queue",
	"random": ["randint", "shuffle"],
	"subprocess": "run",
	"threading": "Thread",
	"time": "sleep",
	"tqdm": "trange",
	"typing": "Optional",
}
# fmt: off
__modules = [
	"os" , "copy", "flask"  , "bisect", "platform", "functools",
	"re" , "html", "heapq"  , "pickle", "requests", "itertools",
	"bs4", "json", "queue"  , "random", "tempfile", "threading",
	"sys", "math", "inspect", "shutil", "textwrap", "contextlib",
			 "stat", "logging", "signal", "tokenize", "subprocess",
			 "time", "pathlib", "socket",             "collections",
			 "tqdm", "typing" , "struct",             "dataclasses",
]
# fmt: on

for module in __modules:
	globals()[module] = importlib.import_module(module)

for module, method in __methods.items():
	if isinstance(method, list):
		for m in method:
			globals()[m] = getattr(importlib.import_module(module), m)
	else:
		try:
			globals()[method] = importlib.import_module(f".{method}", module)
		except Exception:
			globals()[method] = getattr(importlib.import_module(module), method)

if sys.version_info.minor == 9:
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt

	__modules.append("numpy as np")
	__modules.append("pandas as pd")
	__modules.append("matplotlib.pyplot as plt")

__modules.append("importlib")
__modules.append("futures")
print("Populating the namespace with imports:")
pprint(__modules, compact=True)
print("and methods/classes:")
__methodslist = list(__methods.values())
__methodslist.extend(["split_path", "random_"])
pprint(__methodslist, compact=True)

___ignore = """ Not Importing
	# from numba import njit, prange
	# from PIL import Image
	# import cv2
	# import matplotlib.pyplot as plt
	# import numpy as np
	# import pandas as pd
	## from gtts import gTTS
	## from kivy.app import App
	## from kivy.uix.button import Button
	## from kivy.uix.label import Label
	## from operator import attrgetter
	## from urllib import unquote as urlunquote
	## from urllib.parse import unquote as urlunquote
	## from urllib.request import urlopen
	## from user.timeit import timeit
	### from win32com.client import Dispatch
	### from winsound import Beep as beep
	### import imghdr
	### import winreg
"""
if sys.version_info.minor == 9:
	get_ipython().run_line_magic(
		"logstart", "~/Sublime/Ipython_logs/py39log.py rotate"
	)
else:
	get_ipython().run_line_magic(
		"logstart", "~/Sublime/Ipython_logs/log.py rotate",
	)
