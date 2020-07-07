import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import sys

#�������� ����������� � ��
#� �������� ������ ������������ ����� ������
vk_session = vk_api.VkApi(token="05adf63ed2043a20d85c423c27ca8f0f172038227f19418bf3c6cbb89c79bac4831c5d93325d11bc5dfea")
#������� �����������
try:
	#����������� ������ � ������� ������
    vk_session.auth(token_only=True)
#���� �� ������� ��������� �����������
except vk_api.AuthError as error_msg:
	#�� ������� ���������� ��������� �� ������
    print(error_msg)
#����������� ����� API longpoll
longpoll = VkLongPoll(vk_session)
#��������� API ������ ��
vk = vk_session.get_api()

#print(dir(vk))

#sys.exit(0)

T = True
while(T):
	#��������� �� �������
	for event in longpoll.listen():
		#���� ������� - ����� ���������
		#� ��� ���������� ����������
		#� ���� ���� �����
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			#��������, �������� �� ��� � ��			
			if event.from_user:
				#��������� ���������� �� ������������, ������� �������� ���������
				str_id = str(event.user_id) + ','
				user = vk.users.get(user_ids=str_id)
				#������������ ������ 
				mess_text = "�� " + user[0]['first_name'] + " " + user[0]['last_name']
				#����������� ���������
				vk.messages.send(
					#�� ����������
					user_id=event.user_id,
					message=mess_text,
					random_id=random.randint(0, 655546689633) 
					)
				
			#��� ��������� ��������� - ����� �� �������
			sys.exit(0)
		
