from functools import wraps
import time


def timeit(func):
	"""Print the runtime of the decorated function"""

	@wraps(func)
	def time_wrapper(*args, **kwargs):
		start_time = time.perf_counter()
		value = func(*args, **kwargs)
		end_time = time.perf_counter()
		run_time = end_time - start_time
		print(f"Finished {func.__name__}() in {run_time:.2f} secs")
		return value

	return time_wrapper
