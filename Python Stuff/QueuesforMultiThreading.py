import threading
from queue import Queue

userlist = []
user_queue = Queue()


def userlist_manager():
	while True:
		new_user = user_queue.get()
		if newuser not in userlist:
			userlist.append(new_user)
		user_queue.task_done()


user_list_thread = threading.Thread(target=userlist_manager)
user_list_thread.daemon = True
user_list_thread.start()

user_queue.join()

#https://pybay.com/site_media/slides/raymond2017-keynote/threading.html
