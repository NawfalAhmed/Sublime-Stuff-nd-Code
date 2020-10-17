from playsound import playsound as play
from time import sleep
from datetime import datetime
from win32com.client import Dispatch
from winsound import Beep as beep
from gtts import gTTS
import numpy as np

# usgirl = gTTS(text='Good morning', lang='en-us')
# usgirl.save("gm.mp3")
# # play("gm.mp3")
# ukgirl = gTTS(text='Good morning', lang='en-uk')
# ukgirl.save("gm1.mp3")
# # play("gm1.mp3")


def alert(duration=30, beepfreq=400, beeptime=600, beepgap=300):
	"""Duration in secs, beeptime and gap in ms, The Freq is in Hz"""
	for i in range(0, duration * 1000, beeptime + beepgap):
		beep(beepfreq, beeptime)
		sleep((beepgap) / 1000)
	beep(900, 750)


def alarm(hour, mint, timeformat="am", duration=7):
	if timeformat == "pm":
		hour += 12
	currtimeinstr = str(datetime.now()).split()[1].split(":")
	currtime = np.array((int(currtimeinstr[0]), int(currtimeinstr[1])))
	usertime = np.array((hour, mint))
	diff = usertime - currtime
	diff *= 60
	diff[0] *= 60
	sleeptill = np.sum(diff) - int(float(currtimeinstr[-1]))
	if sleeptill >= 0:
		sleep(sleeptill)
	alert(duration, beepgap=600)


alarm(9, 57, "am")

name = "The Song"
# play(name+".mp3")

speak = Dispatch("SAPI.SpVoice")
# for i in range(10):
# sleep(1/10)
# speak.Speak("Sarah Go Sleep!")

# print('\a') # for a windows alert sound
