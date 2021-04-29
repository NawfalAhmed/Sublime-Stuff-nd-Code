marks = [
	["maths", 10], ["english", 70], ["anlsaf", -1], ["economics", 90],
	["physics", 65], ["Urdu", 102]
]
for sub in marks:
	subject = sub[-1]
	if subject > 100:
		print(
			"Bonus marks for handwriting"
			if sub[0] == "Urdu" and subject < 110
			else "error"
		)  # yapf: disable
	elif subject > 90:
		print("A+")
	elif subject >= 80:
		print("A")
	elif subject >= 70:
		print("B")
	elif subject >= 60:
		print("C")
	elif subject >= 50:
		print("D")
	elif subject < 50 and subject >= 0:
		print("F, koi sharam kar!")
	else:
		print("Error")
