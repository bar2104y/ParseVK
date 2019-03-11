import re
from pprint import pprint

#Разовый поиск в строке
def searchOnce(string):
	regEx = re.compile(string)
	while True:
		line = inputFile.readline()
		tmp = re.findall(regEx, line)
		if tmp != []:
			res = tmp[0][1]
			return res

def parseLoginHistory():
	line = ''
	LHArr = []
	while line != '---':
		line = inputFile.readline()
		if line != '\n':
			line = line.replace('\n', '')
			LHArr.append(line)
	del LHArr[len(LHArr)-1]
	return LHArr


path = 'log.txt'
try:
	# Разбор первой строки
	inputFile = open(path, 'r')
	line = inputFile.readline()
	vkID = re.search(r'(vk.com\/id)(.*?)( \()', line)
	vkID = vkID.group(2)
	print('ВК id:',vkID)

	tmp = re.findall(r'(\()(.*?)(\))', line)
	print(tmp)
	personalLink = tmp[0][1]
	print("Личная ссылка:", personalLink)

	name = tmp[1][1]
	print("Имя:", name)

	email = searchOnce('(Email: )(.*)')
	regDate = searchOnce('(Регистрация: )(.*)')
	lastLogin = searchOnce('(Последнее посещение: )(.*)')
	lastIP = searchOnce('(IP-адрес последнего посещения: )(.*)')
	phone = searchOnce('(Телефон: )(.*)')

	print(email)
	print(regDate)
	print(lastLogin)
	print(lastIP)

	inputFile.readline()
	print(parseLoginHistory())
	



	

except IOError:
	print("Ошибка работы с файлом!")
finally:
	inputFile.close()

