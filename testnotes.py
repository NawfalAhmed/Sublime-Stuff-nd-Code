"""
python things to do:

try to turn recursive code to local stack using yield and check the speed too


Try everything in the generators video



python tips:

functions can have private variables that are kinda like static variable for a function in a private class

example
"""

# ------------------------------------------------------------------------------
def store(new: str) -> str:
	try:
		store.history += new + "\n"
	except AttributeError:
		store.history = new + "\n"
	return store.history


for _ in range(1, int(input("Enter Count: "))):
	store(input("Enter Text: "))

print("What you entered was:\n" + store(input("Enter Text: ")))
