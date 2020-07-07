#packet with class vk_api
import vk_1
#packet with convert audio
#for mp3 to Wav
import convert
#packet from aduio parser to string text
import voice
#packet from HTTP request
import urllib
#packet for info with stream for dota2
import dota2request

b = vk_1.vk()

def tryDota2Request(text):
	#Результат разработки
	resText = ""
	topCount = 5
	count = 1
	#Проверка, было ли сообщение, которое касается доты
	if text.lower().find("что по доте") != -1 or text.lower() == "чпд" or text.lower().find("чё по доте") != -1 or text.lower().find("что по dota") != -1:
		#Создание объекта с запросом
		d2r = dota2request.dota2req()
		dict = d2r.getListStream()
		#выбор в словаре только 3 первых ру стрима по доте
		for x in dict:
			if count > topCount:
				continue
			if x['lang'] == 'ru':
				resText += "Стрим: " + x['name'] + '\n'
				resText += "Адрес: " + x['address'] + '\n'
				resText += '\n'
				count += 1
		
		if resText == "":
			resText = "Сейчас нет ру стримов доты"
	return resText

#В данном методе разибраются обычные сообщения
def ParserSimpleMess(e):
			
	#Только одно ключевое слово и один вариант разбора
	text = e.getText()
	res = tryDota2Request(text)
	if res != "":
		e.sendMessage(res)
	

def AudioMess(e):
	try:
		#Получение ссылки на сообщение
		url = e.getLinkAudio()['mp3']
		#Скачивание файла в формате mp3
		urllib.request.urlretrieve(url, '1.mp3')
		#Конвертация 
		convert.ConvertMp3ToWav('1.mp3', '1.wav')
		#Получение текста
		text = voice.audioToText('1.wav')
		#Если не удалось разобрать
		if text == None: 
			#Отправить сообщение об неудаче
			text = 'Не удалось разобрать'
		
		#Если сказали - что по доте или синоним
		res = tryDota2Request(text)
		
		#Получение имени пользователя
		name = e.getInfUser()['fn']
		#Отправление сообщения
		e.sendMessage(name + ': ' + text)
		#А теперь дота
		if res != "" :
			#Отправление сообщения, конец обработки
			res = "А теперь - дотка:\n" + res
			e.sendMessage(res)
	except BaseException:
		print(BaseException.args)
		pass

#add function for receiving message with audio message
#after function send dialog text audio message
b.setFromGroupAudioMess(AudioMess)

b.setfFromGroupSimpleMess(ParserSimpleMess)

b.AythToToken()
b.Start()
