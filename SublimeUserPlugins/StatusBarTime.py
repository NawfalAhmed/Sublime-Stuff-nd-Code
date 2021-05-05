import sublime
from time import sleep
from threading import Thread
from datetime import datetime

alive = False


def plugin_loaded() -> None:
	global alive
	alive = True
	update_interval = 30  # secs
	start_time = datetime.now().strftime("%j,%H,%M").split(',')

	settings = sublime.load_settings('StatusBarTime.sublime-settings')
	formatt = settings.get('StatusBar_Format', "%I:%M %p")
	up_time = settings.get('StatusBar_UpTime', True)
	Thread(
		target=time_printer,
		args=(formatt, up_time, update_interval, start_time),
		daemon=True
	).start()


def plugin_unloaded() -> None:
	global alive
	alive = False


def time_printer(formatt, up_time, update_interval, start_time):
	while alive:
		time = datetime.now()
		view = sublime.active_window().active_view()
		current = time.strftime("%j,%H,%M").split(',')
		day, hr, minute = map(lambda x, y: int(x) - int(y), current, start_time)
		view.set_status("__statustime", time.strftime(formatt))
		if up_time:
			view.set_status(
				"__statusuptime", str(day*24*60 + hr*60 + minute) + " minutes"
			)
		sleep(update_interval)
