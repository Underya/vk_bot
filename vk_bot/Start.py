import getpass
import shutil
import os
import os.path as path

#Глобальная переменная с именем bat файла
name_bat_file = "vk_bot.bat"

#Получение адресса 
def GetStartAddress():
    userName = getpass.getuser()
    path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % userName
    return path

#Проверка, существует ли папка с указанным адрессом    
def CheckStartAddress():
    dir_path = GetStartAddress()
    return path.exists(dir_path)

#Создание файла батника, который запускает бота
#Параметр - имя файла, который запускает бота
def CreateBatFile(file_name):
    #Создание bat файла
    f = open(name_bat_file, "w")
    #Получение адреса текущей папки
    c_dir = os.getcwd()
    #Получение полного адресса файла 
    full_dir = c_dir + "\\" + file_name
    #Запись пути в файл
    f.write(full_dir)
    #Закрыть файл после записи
    f.close()
    

#Выполнение функций модуля
if __name__ == "__main__":

    #Установка всех модулей, необходимых для работы бота вк
    os.system("pip install vk_api")
    os.system("pip install pydub")
    os.system("pip install SpeechRecognition")
    
    #Попытка закинуть батник в папку автозапуска
    #Проверка, получилось ли найти нужную папку
    if CheckStartAddress():
        #Если папка существует, то в неё копируется файл
        spath = GetStartAddress()
        #Создние самого файла
        CreateBatFile("b.py")
        shutil.copy(name_bat_file, spath)
    else:
        print("Not find start up directory!\n")

    print("Install End!\n")
    input("Press Enter to continue")
	
