import sublime
import sublime_plugin
from time import sleep
from threading import Thread
from datetime import datetime
from os.path import expanduser

log_path = expanduser(r"~/Sublime/SublimeUpTime.log")
alive = False
total_up_time = None


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
	with open(log_path, "a") as logger:
		time = datetime.now()
		log = total_up_time + time.strftime(" on %A _ %B, %Y (logged@%#I:%#M|)")
		check = {"1": "st", "2": "nd", "3": "rd"}
		day = time.strftime("%#d")
		day += check.get(day[-1], "th")
		log = log.replace("_", day).replace("|", time.strftime("%p").lower())
		logger.write(log + "\n")


class OnExitListener(sublime_plugin.EventListener):

	def on_exit(self):
		plugin_unloaded()


def time_printer(formatt, up_time, update_interval, start_time):
	global total_up_time
	while alive:
		time = datetime.now()
		view = sublime.active_window().active_view()
		current = time.strftime("%j,%H,%M").split(',')
		day, hr, minute = map(lambda x, y: int(x) - int(y), current, start_time)
		view.set_status("__statustime", time.strftime(formatt))
		if up_time:
			total_up_time = str(day*24*60 + hr*60 + minute) + " minutes"
			view.set_status("__statusuptime", total_up_time)
		sleep(update_interval)
