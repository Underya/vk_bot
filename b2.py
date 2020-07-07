import vk_1
import convert
import voice
import urllib

b = vk_1.vk()

def AudioMess(e):
	try:
		
		url = e.getLinkAudio()['mp3']
		
		urllib.request.urlretrieve(url, '1.mp3')
		
		convert.ConvertMp3ToWav('1.mp3', '1.wav')
		
		text = voice.audioToText('1.wav')
		
		if text == None: 
		
			text = 'Не удалось разобрать'
		
		name = e.getInfUser()['fn']
		
		e.sendMessage(name + ': ' + text)
	except BaseException :
		pass

b.setFromGroupAudioMess(AudioMess)

b.AythToToken()
b.Start()