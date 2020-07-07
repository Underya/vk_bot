
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

import random

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class vk_event:
	

	d_event = None


	def __init__(self, event, vk_api):

		self.e = event

		self.vk = vk_api
		

	def getEvent(self):

		e = self.e

		d = {}

		d['text'] = e.text
		d['attach'] = e.attachments

		d['from_id'] = e.from_id		

		d_event = d
		return d
		

	def getAttach(self):

		if self.d_event == None:

			self.getEvent()

		return self.d_event['attach']
		

	def isAudioMess(self):

		
		
		if self.d_event == None:
		
			self.getEvent()
		
		
		a = self.d_event['attach']
		
		if a == None or len(a) == 0: return False
		
		a = a[0]
		
		if a['type'] == "audio_message":
		
			return True
		else:
		
			return False
		
	
	def getLinkAudio(self):
	
	
		a = self.getAttach()[0]['audio_message']
	
		ret = {}
	
		ret['mp3'] = a['link_mp3']
		ret['ogg'] = a['link_ogg']
	
		return ret
	
	
	def getInfUser(self):
	
		user = self.vk.users.get(user_ids=self.d_event['from_id'])[0]
	
		ret = {}
	
		ret['id'] = user['id']
	
		ret['fn'] = user['first_name']
	
		ret['ln'] = user['last_name']
		
		return ret
		
	
	

class vk_g_event(vk_event):


	def getEvent(self):

		e = self.e.object

		d = {}

		d['text'] = e.text
		d['attach'] = e.attachments

		d['from_id'] = e.from_id

		d['peer_id'] = e.peer_id

		self.d_event = d
		return d
		

	def sendMessage(self, text):		


		self.vk.messages.send(peer_id=self.d_event['peer_id'], 
		message=text,
		random_id=0)




class vk:
	

	f_fromToMe = None

	f_fromToMeAudioMess = None

	f_fromGroupAudioMess = None
	

	vk_session = None
	

	def setFromToMe(self, function):
		self.f_fromToMe = function
	

	def setFromToMeAudio(self, function):
		self.f_fromToMeAudioMess = function
		

	def setFromGroupAudioMess(self, function):
		self.f_fromGroupAudioMess = function
		

	def AythToToken(self, token_v = "e7ddcb5c4e21dd9c0c751c70190c32dea8d6413e7ddddff9c8dc295a304825806dc18e4a15896541e25b2"):

		self.token = token_v
		#e7ddcb5c4e21dd9c0c751c70190c32dea8d6413e7ddddff9c8dc295a304825806dc18e4a15896541e25b2
		#"05adf63ed2043a20d85c423c27ca8f0f172038227f19418bf3c6cbb89c79bac4831c5d93325d11bc5dfea"

		self.vk_session = vk_api.VkApi(token=token_v)
		

		try:

			self.vk_session.auth(token_only=True)
			
			ret_v = None
		except vk_api.AuthError as error_msg:
			
			print(error_msg)
			
			ret_v = error_msg
					
		
		
		return ret_v
		
	
	
	def Start(self):
	
	
		if self.vk_session == None:
	
			raise Exception("Не произведена авторизация")
			
	
		self.longpoll = VkLongPoll(self.vk_session)

	
		self.vk = self.vk_session.get_api()
		
	
		self.glongpoll = VkBotLongPoll(vk=self.vk_session, group_id='185478915')
		
	
		while True:
			
	
			for event in self.glongpoll.listen():
				print("Прошло групповое событие")
	
				e = vk_g_event(event, self.vk)
				
	
				if event.type == VkBotEventType.MESSAGE_NEW:
				
	
					if self.f_fromGroupAudioMess != None:
					
	
						if e.isAudioMess():
							self.f_fromGroupAudioMess(e)
						
						
			
			continue
			
			
			for event in self.longpoll.listen():				
			
				print('Сообщение пришло')
			
				e = vk_event(event, self.vk)
				
			
				if self.f_fromToMeAudioMess != None:
					pass
					
			
				if self.f_fromToMe != None:
			
					if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
						
			
						self.f_fromToMe(e)
			
						continue
				
				print('Сообщение пошло на проверку')
			
				if self.f_fromGroupAudioMess != None:
			
					if event.type == VkEventType.MESSAGE_NEW and event.from_chat: 
			
						att = event.attachments	
						print(att)
			
						if att['attach1_kind'] == 'audiomsg':
			
							self.f_fromGroupAudioMess(e)
							continue
		
