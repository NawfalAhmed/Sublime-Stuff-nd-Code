import os

path = os.path.expandvars("%SublimeText%").replace("\\", "/")
emptydirs = [
	dirpath.replace(path, "").replace("\\", "/")
	for (dirpath, dirname, filename) in os.walk(path)
	if not len(dirname) + len(filename) and ".git" not in dirpath
]

print(*emptydirs, sep="\n")
if emptydirs and input("Remove Empty Folders? : ").lower() in ("yes", "y"):
	for emptydir in emptydirs:
		os.system(f'rmdir "{path+emptydir}"')
