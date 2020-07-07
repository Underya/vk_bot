#Функция конвертирует файл из mp3 в wav
#inname - полное имя входного файла в формате mp3
#outname - полное имя выходного файла в формате wav
#Функция создаёт файл сразу на диске, и возвращает полное имя выходного файла
def ConvertMp3ToWav(inname, outname):
    #Импорт библиотике для конвертирования
    from pydub import AudioSegment
    #Получение аудио из файла
    sound = AudioSegment.from_mp3(inname)
    #Конвертирование с новым именем
    sound.export(outname, format='wav')
    #Возвращение имени файла
    return outname
