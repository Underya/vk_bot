import speech_recognition as sr
import os
import sys
import webbrowser


#Функция преобразования из звука в текст
#file - Имя файла в формате wav, который будет преобразован в текст
#Возвращает текст в формате строки, или None, если преобразование не получилось
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