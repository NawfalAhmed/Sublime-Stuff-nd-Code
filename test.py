from glob import glob
from os import path
from pathlib import Path, PurePath

path = PurePath("Users/Ibraheem/Desktop/SublimeText/AI/test.py")

print("/".join(path.parts[path.parts.index("SublimeText") + 1:]))

# txtfiles = glob("*")

# print(type(txtfiles))
