myfile = open("meh.txt", 'r')
save = myfile.read()
save = save.split()
name = str(input("enter the sentance\n"))
name = name.split()
for word in name:
	if word not in save:
		print(word, "is incorrect")
myfile.close()
