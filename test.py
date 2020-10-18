from glob import glob
from os import path
from pathlib import Path, PurePath

path = PurePath("Users/Ibraheem/Desktop/SublimeText/AI/test.py")
txtfiles = glob("*")

print("/".join(path.parts[path.parts.index("SublimeText") + 1:]))
print(txtfiles)
