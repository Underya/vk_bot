#Получение API самого контакта
import vk_api
#Получение отдельно API для получения событий
from vk_api.longpoll import VkLongPoll, VkEventType
#Подключение функции для получения id_сообщения
import random
#Подключение класса для работы с беседами, в которых состоит бот
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
#Инициализация бота для работы с ВК		

#Класс ВК евента
class vk_event:
	
	#Словарь информации о событии 
	d_event = None

	#Конструктор экземпляра класса
	def __init__(self, event, vk_api):
		#Сохранение указателя на event
		self.e = event
		#сохранение указателя на апи в вк
		self.vk = vk_api
	
	#Получение текста сообщения
	def getText(self):
		return self.d
		return self.d['text']
		
	#Получение сообщения об событии в форме словаря
	def getEvent(self):
		#Для сокращённого вызова
		e = self.e
		#Словарь с параметрами, который надо вернуть
		d = {}
		#Заполнение словаря
		d['text'] = e.text
		d['attach'] = e.attachments
		#ID того, от КОГО пришло сообщение
		d['from_id'] = e.from_id		
		#Сохранение словаря внутри класса
		d_event = d
		return d
		
	#Получение только приложения к сообщению
	def getAttach(self):
		#Проврек, был ли словарь
		if self.d_event == None:
			#Если не было словаря, вызвать функцию для заполнения
			self.getEvent()
		#Вернуть приложение 
		return self.d_event['attach']
		
	#Метод возврщает True, если событие - аудио сообщение
	def isAudioMess(self):
		#Получение информации из словаря
		
		#Проверка, был ли заполнен словарь
		if self.d_event == None:
			#Если не заполнен, то вызывается метод для заполнения
			self.getEvent()
		
		#Получение массива с приложениями к 
		a = self.d_event['attach']
		#Если вернулся пустой массив - точно не аудио приложение
		if a == None or len(a) == 0: return False
		#Если аудио сообщение, то это словарь, первый в массиве
		a = a[0]
		#Проврека, какаой тип у приложения
		if a['type'] == "audio_message":
			#Если совпдает - то сообщение аудио сообщение
			return True
		else:
			#Если нет, то это не аудио сообщение
			return False
		
	#Получение ссылок на скачивание 
	def getLinkAudio(self):
		#Считаем, что пользователь уже проверил на аудио сообщение
		#получение информации о самом аудио сообщение
		a = self.getAttach()[0]['audio_message']
		#Словарь, который будет возвращён
		ret = {}
		#Получение ссылок
		ret['mp3'] = a['link_mp3']
		ret['ogg'] = a['link_ogg']
		#Возвращение словаря со ссылками
		return ret
	
	#Получение информации о пользователе, который отправил сообщение
	def getInfUser(self):
		#Получение общей ифнормации о пользователе
		user = self.vk.users.get(user_ids=self.d_event['from_id'])[0]
		#Создание словаря с информацией
		ret = {}
		#ИД
		ret['id'] = user['id']
		#Имя
		ret['fn'] = user['first_name']
		#Фамилия
		ret['ln'] = user['last_name']
		#Вернуть информацию
		return ret
		
	
	
#Класс, события, но для 
class vk_g_event(vk_event):

	#Получение сообщения об событии в форме словаря
	def getEvent(self):
		#Для сокращённого вызова
		e = self.e.object
		#Словарь с параметрами, который надо вернуть
		d = {}
		#Заполнение словаря
		d['text'] = e.text
		d['attach'] = e.attachments
		#ID того, от КОГО пришло сообщение
		d['from_id'] = e.from_id
		d#ID беседы, из которой пришло сообщенние
		d['peer_id'] = e.peer_id
		#Сохранение словаря внутри класса
		self.d_event = d
		return d
		
	def getText(self):
		return self.d_event['text']
	
	#Отправление сообщения в ту беседу, откуда получено событие
	def sendMessage(self, text):		
		#Отправление сообщения
		#Отправление в группу
		self.vk.messages.send(peer_id=self.d_event['peer_id'], 
		message=text,
		random_id=0)
		#random_id=random.randint(0, 92233720368547758072))

#Класс, который реализует чат бота
#Ему необходимо передовать функции со входным параметром типа класса события
#Функции будут вызываться при соотвествующем событии
class vk:
	
	#Свойства-атрибуты класса, являющиеся функциями, вызываемые при соответствующем событии
	#Должны иметь только один входной параметр, куда будет передан экземпляр класса события
	#Функция, которая вызывается при получении в личку сообщения 
	f_fromToMe = None
	#Функция, которая вызывается при получении в личку аудиоо сообщения
	f_fromToMeAudioMess = None
	#Функция, которая вызывается при получнеии голосовухи в беседе
	f_fromGroupAudioMess = None
	#function, which is called upon receipt simple message
	f_fromSimpleGroupMess = None
	#Объект сессии, используемоей классом для взаимодействия с вк
	vk_session = None
	
	#Метод устаналивает функцию, вызываемую при получению сообщению боту в личку
	def setFromToMe(self, function):
		self.f_fromToMe = function
	
	#Метод устаналивает функцию, вызываемую при получнии аудио-сообщения в личку
	def setFromToMeAudio(self, function):
		self.f_fromToMeAudioMess = function
		
	#Метод устаналивает функцию, вызываемую при получнии аудио-сообщения в груповой беседе
	def setFromGroupAudioMess(self, function):
		self.f_fromGroupAudioMess = function
		
	#Метод устаналивает функцию, которая вызывается при получении обычного сообщения
	def setfFromGroupSimpleMess(self, function):
		self.f_fromSimpleGroupMess = function
	
	#Метод для авторизации через токен
	def AythToToken(self, token_v = "e7ddcb5c4e21dd9c0c751c70190c32dea8d6413e7ddddff9c8dc295a304825806dc18e4a15896541e25b2"):
		#Токен моей группы, что бы не забыть
		self.token = token_v
		#e7ddcb5c4e21dd9c0c751c70190c32dea8d6413e7ddddff9c8dc295a304825806dc18e4a15896541e25b2
		#"05adf63ed2043a20d85c423c27ca8f0f172038227f19418bf3c6cbb89c79bac4831c5d93325d11bc5dfea"
		#Создание сессии группы в вк по токену
		self.vk_session = vk_api.VkApi(token=token_v)
		
		#Попытка авторизации сесии
		try:
			#Функция авторизации по токену
			self.vk_session.auth(token_only=True)
			#Если сессия авторизирована нормально, возвращется None
			ret_v = None
		except vk_api.AuthError as error_msg:
			#Если не вышло - вывести ошибку
			print(error_msg)
			#И вернуть текст ошибки
			ret_v = error_msg
					
		
		#Возвращение результатов авторизации
		return ret_v
		
	
	#Метод, который запускает чат-бота
	def Start(self):
	
		#Проверка, была ли авторизация
		if self.vk_session == None:
			#Выкинуть исключение
			raise Exception("Не произведена авторизация")
			
		#Инициализация бота для работы с ВК		
		self.longpoll = VkLongPoll(self.vk_session)

		#Получение класса VK_Api
		self.vk = self.vk_session.get_api()
		
		#Получение класса сессии для группового диалога		
		self.glongpoll = VkBotLongPoll(vk=self.vk_session, group_id='185478915')
		
		#Бесконечный цикл, в ходе которого и происходит работа бота		
		while True:
			
			#Получение всех сообщений из бесед с ботом 
			for event in self.glongpoll.listen():
				print("Прошло групповое событие")
				#Создание объекта класса события
				e = vk_g_event(event, self.vk)
				
				#Событие - новое сообщение, адресовано боту, у него не пустой текст, и оно направлено в личку
				if event.type == VkBotEventType.MESSAGE_NEW:
				
					#Check, this message - is audio message
					if e.isAudioMess():
				
						#Если указана функция проверки на аудио сообщения
						if self.f_fromGroupAudioMess != None:
											
							self.f_fromGroupAudioMess(e)
							#if is audio message - end parser this message
							continue
						
					#if message - is simple message
					#check parser from simple message
					if self.f_fromSimpleGroupMess != None:
						print("simple mess")
						self.f_fromSimpleGroupMess(e)
							
			#Для откладки - конец цикла
			continue
			
			#В начале очереди получаем все события из лички, что лежат на сервере
			for event in self.longpoll.listen():				
				#Если есть события, то проводиться поиск подходящего события
				#Сначала проверяется, есть ли обработчки данного события
				#И если есть - проверка условий
				print('Сообщение пришло')
				#Создание объекта класса события
				e = vk_event(event, self.vk)
				
				#Проверка на аудио сообщение в личку				
				if self.f_fromToMeAudioMess != None:
					pass
					
				#Проверка на обычное сообщение в личку
				if self.f_fromToMe != None:
					
					#Событие - новое сообщение, адресовано боту, у него не пустой текст, и оно направлено в личку
					if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
						
						#Вызов события
						self.f_fromToMe(e)
						#Конец проверок, переход к следующему событию
						continue
				
				print('Сообщение пошло на проверку')
				#Проверка на аудио сообщение в беседе
				if self.f_fromGroupAudioMess != None:
					#Пока - все сообщения проверяются на аудио
					if event.type == VkEventType.MESSAGE_NEW and event.from_chat: 
						#Проверка, конкретно ли это аудио
						#Сохранение поля с прекреплёнными сообщениями
						att = event.attachments	
						print(att)
						#И оно равно значению audiomsg, типа аудио-сообщения
						if att['attach1_kind'] == 'audiomsg':
							#Вызов события
							self.f_fromGroupAudioMess(e)
							continue
		
#Старый текст, что бы не забыть, как с этим работать
"""
while(False):
	vk = vk_api
	#Получение очереди событий
	for event in longpoll.listen():
		#Если событие имеет тип нового события
		#И оно адресовано группе
		#И у него есть текст
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			#Если новое сообщение из лички группы
			if event.from_user:
				#Пользователю отправляется тестовое сообщение
				str_id = str(event.user_id) + ','
				user = vk.users.get(user_ids=str_id)
				mess_text = "Ты " + user[0]['first_name'] + " "+user[0]['last_name']   
	
				vk.messages.send(user_id=event.user_id,message=mess_text,random_id=random.randint(0, 92233720368547758072))
				vk.messages.send(user_id=event.user_id,message=event.text,random_id=random.randint(0, 92233720368547758072))			
				#Пока идёт тест, отключение после 1 сообщения
				exit(0)
		#Попытка поймать любое сообщение
		if event.type == VkEventType.MESSAGE_NEW:			
			#Содержимое среди поля attachments идёт поиск поддтипа audiomsg
			#Сохранение поля в переменную
			att = event.attachments						
			
			#Если есть это свойство
			if "attach1_kind" in att:
				#И оно равно значению audiomsg, типа аудио-сообщения
				if att['attach1_kind'] == 'audiomsg':
					#Получение нормальноый ссылки на сообщение
					mess = vk.messages.getById(message_ids=str(event.message_id) + ',')			
					mess = mess['items'][0]
					#Из сообщения получаем ссылку, по которой можно аудиозапись скачать					
					att2 = mess['attachments'][0]['audio_message']
					url = att2['link_mp3']
					#И на всякий случай ключ доступа
					access_key = att2['access_key']									
					#Скачивание файла в mp3
					urllib.request.urlretrieve(url, '123.mp3')
					convert.ConvertMp3ToWav('123.mp3', '1.wav')
					#Преобразование
					text = voice.audioToText('1.wav')
					#Формирование сообщения для отправки пользователю
					mess_text = ""
					#Если сообщение не удалось разобрать
					if text == None:
						mess_text = "Сообщение не удалось разобрать"
					else:
						#Получение имени пользователя
						str_id = str(event.user_id) + ','
						user = vk.users.get(user_ids=str_id)
						us_name = user[0]['first_name']
						mess_text = us_name + ": " + text
					#Отправление сообщения
					vk.messages.send(user_id=event.user_id,message=mess_text,random_id=random.randint(0, 92233720368547758072))
"""