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
	#Конструктор экземпляра класса
	def __init__(self, event, vk_api):
		#Сохранение указателя на event
		self.e = event
		#сохранение указателя на апи в вк
		self.vk = vk_api
		
	#Получение сообщения об событии в форме словаря
	def getEvent(self):
		#Для сокращённого вызова
		e = self.e
		#Словарь с параметрами, который надо вернуть
		d = {}
		#Заполнение словаря
		d['text'] = e.text
		d['attach'] = e.attachments
		return d
	
	

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
				e = vk_event(event, self.vk)
				
				
				print(event.type)
				#Событие - новое сообщение, адресовано боту, у него не пустой текст, и оно направлено в личку
				if event.type == VkBotEventType.MESSAGE_NEW:
					#Если есть это свойство
					print(e.getEvent()["attach"])
						
						
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