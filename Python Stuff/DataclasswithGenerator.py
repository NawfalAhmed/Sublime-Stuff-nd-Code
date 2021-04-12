from dataclasses import dataclass


@dataclass
class Student:
	"""Student info"""
	sid: str
	name: str
	age: int
	degree: str
	cgpa: float
	address: str


def details():
	print("Enter Student details:")
	yield input("Enter sid: ")
	yield input("Enter name: ")
	yield int(input("Enter age: "))
	yield input("Enter degree: ")
	yield float(input("Enter cgpa: "))
	yield input("Enter address: ")


std = Student(*details())  # iterables can be unpacked when passing
# as function parameters

print(std)
