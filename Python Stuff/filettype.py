import filetype
while True:
	val = input("enter:")
	kind = filetype.guess(val)
	if kind is None:
		print('Cannot guess file type!')
		break
	else:
		print('File extension: %s' % kind.extension)
		print('File MIME type: %s' % kind.mime)
