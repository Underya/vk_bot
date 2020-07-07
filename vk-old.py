#Получение API самого контакта
import vk_api
#Получение отдельно API для получения событий
from vk_api.longpoll import VkLongPoll, VkEventType
#Подключение функции для получения id_сообщения
import random
#Библиотека для скачивания файлов по URL
#Слава сатане, хотя бы встроенная
import urllib.request
#Подключение модуля для конвертирования из mp3 в Wav
import convert
#Подключение модуля с функцией преобразования из аудио файла в текст
import voice

#Создание сессии группы в вк по токену
vk_session = vk_api.VkApi(token="05adf63ed2043a20d85c423c27ca8f0f172038227f19418bf3c6cbb89c79bac4831c5d93325d11bc5dfea")

#Попытка авторизации сесии
try:
	#Функция авторизации по токену
	vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
	#Если не вышло - вывести ошибку
	print(error_msg)

#Получение класса для запросов к вк
longpoll = VkLongPoll(vk_session)

#Получение класса VK_Api
vk = vk_session.get_api()


#Переменная для цикла
T = True
#Полубесконечный цикл
while(T):
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