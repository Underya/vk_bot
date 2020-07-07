#Данный модуль реализует класс, который совершает запрос к сайту с информацией о доте 2 

#Сайт, на котором есть информация о текущих стримах по доте
#https://game-tournaments.com/dota-2
#объект на страничцке, внутри которого располагаются текущие активные стримы по доте
#ul id="index_stream"
#Тег, внутри которого название трансялции. Сам тег вложен в тег с инфой о стриме
#<div class="sinfo">
#Где то за ним идёт тег <u>
#Тег класса языка трансляции
#class="slang">

#библиотека для для работы по протоколу HTTP
import urllib.request as request
import urllib.parse as parse

class dota2req:
	
	#Конструктор объекта
	#Происходит запрос к сайту 
	#И сохранение в поле класса текста страницы
	def __init__(self):
		#КОНСТАНТЫ ДЛЯ ДАННОГО САЙТА
		#Константа с адресом сайта
		self.__dotaSite = r"https://game-tournaments.com/dota-2"
		#Константа с указателем, на объект в котором содержаться стримы
		self.__classContainer = 'ul id="index_stream"'
		#константа, в которой хранится название атрибута, который соержит имя канала
		self.__attNameStream = "data-original-title"
		#Константа, в которой хранится тег названия трансляции
		self.__attOrigName = '<div class="sinfo">'
		#Тег языка трансляции
		self.__tagLang = 'class="slang">'
		#Заполнение поля с текстом сайта
		self.__site = str(self.__request(self.__dotaSite))
			
		
	#Метод производит запрос к указаному сайту и сохраняет его результат в своём поле
	def __request(self, site):
		#Создание заголовка для запроса к странице
		req = request.Request(site, headers={'User-Agent' : "Magic Browser"})
		#Запрос и получение объекта, с помощью которого происходит получение содержимого страницу
		con = request.urlopen(req)
		#Возврат текста страницы
		return con.read()
	
	#Метод получает информацию о стриме по строке, 
	def __getStreamInd(self, site, indexNameStream):
		#Информация о стриме
		streamInf = {}
		
		#Получение адреса трансляции
		#Индекс двойных кавычек
		indexFirstQuotes = site.find('"', indexNameStream, indexNameStream + 100)
		indexLastQuotes = site.find('"', indexFirstQuotes + 1, indexFirstQuotes + 100)
		#Сохранение адреса
		streamInf["address"] = r"https://www.twitch.tv/" + site[indexFirstQuotes + 1 : indexLastQuotes]
		
		#Получение языка трансляции
		firstIndex = site.find(self.__tagLang, indexNameStream)
		firstIndex = firstIndex + len(self.__tagLang)
		lastIndex = site.find("<", firstIndex)
		streamInf["lang"] = site[firstIndex: lastIndex].lower()
		
		#Получение название трансляции
		firstIndex = site.find(self.__attOrigName, indexNameStream)
		firstIndex = site.find("<u>", firstIndex)
		firstIndex += len("<u>")
		lastIndex = site.find("</u>", firstIndex)
		#Получение строки с назваим
		stringName = site[firstIndex: lastIndex]
		#stringName = stringName.encode()
		#Проверка, нет ли лишних символов
		#if '\xd0' :
		#	slechInd = stringName.find('\xd0')
		#	stringName = stringName[:slechInd]
			
		streamInf['name'] = parse.unquote(stringName.replace("\\x","%", 20000))
				
		#Возвращение результата
		return streamInf
	
	#Метод возвращает список русских стримов
	def getListStream(self):
		#Переменная для ру стримов
		listStream = []
		#Поиск в тексте страницы объекта, внутри которого объекты со стримом
		indexCont = self.__site.find(self.__classContainer)
		
		nextInd = indexCont
		#Разбор всех стримов в этом объекте
		while True:
			#Поиск среди объектов всех, которые содержат название трансляции
			data_index = self.__site.find(self.__attNameStream, nextInd)
			
			if data_index == -1:
				break
			
			#Обработка найденного варианта			
			res =  self.__getStreamInd(self.__site, data_index)
			
			#Добавление объекта к списку стримов
			listStream.append(res)
						
			#Переход к следующему элементу
			nextInd = data_index + 1	
			
			#Если нет больше вариантов, или перешли к более ранним вариантам, которые НЕ содержатся в блоке
			if indexCont > nextInd : 
				break
	
	
		#Возвращение списка стримов		
		return listStream
