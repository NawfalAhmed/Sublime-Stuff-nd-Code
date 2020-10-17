from numba import njit
from tqdm import trange


@njit
def func():
	for i in range(1000_000):
		pass


for i in trange(10000):
	func()
