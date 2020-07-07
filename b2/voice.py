import speech_recognition as sr
import os
import sys
import webbrowser



def audioToText(file):
	r = sr.Recognizer()
	a = sr.AudioFile(file)
	with a as h:
		aud = r.record(h)
		text = ""
		try:
			text = r.recognize_google(aud, language="ru-RU")
		except:
			text = None
	return text