import requests

path = "Result/"
name = "image"
ext = ".jpg"
outext = ".png"

for i in ('1', '2'):
	response = requests.post(
		'https://api.remove.bg/v1.0/removebg',
		files={'image_file': open(name + i + ext, 'rb')},
		data={'size': 'auto'},
		headers={'X-Api-Key': '8F5NZTmr74r4g3KnKu9w6pU5'},
	)
	if response.status_code == requests.codes.ok:
		with open(path + name + i + outext, 'wb') as out:
			out.write(response.content)
	else:
		print("Error:", response.status_code, response.text)

print("Done")
