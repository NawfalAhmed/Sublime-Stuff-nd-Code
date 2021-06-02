list1, list2 = [3, 2, 5], [2, 4, 1]
list1, list2 = map(
	list, (zip(*sorted(zip(list1, list2, strict=True), reverse=True)))
)
print(list1, list2)


class Point:
	def __init__(self, x, y, z=None):
		self.x = float(x) if isinstance(x, str) else x
		self.y = float(y) if isinstance(y, str) else y
		self.xy = (self.x, self.y)

	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError("Out of Range")


p = Point(4, 6)
print(*p)
