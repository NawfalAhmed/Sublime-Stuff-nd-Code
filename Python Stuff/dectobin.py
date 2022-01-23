def decimaltobinary(number: int):
	half = number
	power = 1
	ans = 0

	while half > 0:
		ans += (half % 2) * power
		power *= 10
		half //= 2
	return ans


print(decimaltobinary(12))
