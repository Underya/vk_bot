import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import sys

#Создание подключения с ВК
#В качестве токена используется токен Группы
vk_session = vk_api.VkApi(token="05adf63ed2043a20d85c423c27ca8f0f172038227f19418bf3c6cbb89c79bac4831c5d93325d11bc5dfea")
#Попытка подключения
try:
	#Авторизация только с помощью токена
    vk_session.auth(token_only=True)
#Если не удалось выполнить подключение
except vk_api.AuthError as error_msg:
	#На консоль выводиться сообщение об ошибке
    print(error_msg)
#Подключение через API longpoll
longpoll = VkLongPoll(vk_session)
#Получение API самого ВК
vk = vk_session.get_api()

#print(dir(vk))

#sys.exit(0)

T = True
while(T):
	#Прослушка на события
	for event in longpoll.listen():
		#Если событие - новое сообщение
		#И оно адерсовано сообществу
		#У него есть текст
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			#Проверка, написано ли оно в ЛС			
			if event.from_user:
				#Получение информации об пользователе, который отправил сообщение
				str_id = str(event.user_id) + ','
				user = vk.users.get(user_ids=str_id)
				#Формирование текста 
				mess_text = "Вы " + user[0]['first_name'] + " " + user[0]['last_name']
				#Отправление сообщения
				vk.messages.send(
					#Ид сообщества
					user_id=event.user_id,
					message=mess_text,
					random_id=random.randint(0, 655546689633) 
					)
				
			#При получении сообщения - выход из скрипта
			sys.exit(0)
		
