def find(number: int):
	valueset = [(int("1" * x) % number) for x in range(1, number + 1)]
	try:
		print("1" * (valueset.index(0) + 1))
	except:
		for remainder in valueset:
			indices = [i for i, x in enumerate(valueset) if x == remainder]
			if len(indices) >= 2:
				print(int("1" * (indices[1] + 1)) - int("1" * (indices[0] + 1)))
				break


find(132)
