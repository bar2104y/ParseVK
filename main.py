import re
from pprint import pprint

def skipLines():
	line = ''
	inputFile.readline()
	while line != '---\n':
		line = inputFile.readline()

#Разовый поиск в строке
def searchOnce(string):
	regEx = re.compile(string)
	while True:
		line = inputFile.readline()
		tmp = re.findall(regEx, line)
		if tmp != []:
			res = tmp[0][1]
			return res

def parseBlock():
	line = ''
	Arr = []
	while line != '---':
		line = inputFile.readline()
		if line != '\n':
			line = line.replace('\n', '')
			Arr.append(line)
	del Arr[len(Arr)-1]
	return Arr

#Получение списка друзей
# Return [[link, name],
#		  [link, name]]
def parseFriends():
	line = ''
	Arr = []
	inputFile.readline()
	while line != '---':
		line = inputFile.readline()
		if line != '\n':
			line = line.replace('\n', '')
			tmp = line.split(' ')
			Arr.append(tmp)
	del Arr[len(Arr)-1]
	for t in Arr:
		t[1] = t[1].replace('(', '')
		t[2] = t[2].replace(')', '')

	del Arr[len(Arr)-1]
	return Arr

def parseMessages():
	global vkID
	line = ''
	stopString = 'Сообщения, оставленные на стене пользователя https://vk.com/id'+vkID+':\n'
	
	Arr = []
	flag = False
	while line != stopString and not flag:
		while line != 'От кого:\n' and line != 'Кому:\n':
			line = inputFile.readline()
		# message info 
		# [direction(0 in; 1 out), userlink, date, message]
		tmp = []
		if line == 'От кого:\n':
			tmp.append(0)
		else:
			tmp.append(1)

		line = inputFile.readline()
		
		if re.findall(r'Пользователь',line) != []:
			userlink = re.search(r'(https://vk.com/id)(.*)?', line)
			userlink = str(userlink.group()).replace(')', '')
			#print(userlink)
			tmp.append(userlink)
			tmp.append(str(inputFile.readline()).replace('\n', ''))

			mes = ''
			while line != '\n':
				line = inputFile.readline()
				if line == stopString:
					flag = True
					line = ''
				mes += line
			
			tmp.append(mes.replace('\n', ''))
		else:
			while line != '\n':
				line = inputFile.readline()
				if line == stopString:
					flag = True
		Arr.append(tmp)
	print('all')
	return Arr
		
		

# def parseLoginHistory()link, name:
# 	line = ''
# 	LHArr = []
# 	while line != '---':
# 		line = inputFile.readline()
# 		if line != '\n':
# 			line = line.replace('\n', '')
# 			LHArr.append(line)
# 	del LHArr[len(LHArr)-1]
# 	return LHArr

# def parseNameHistory():
# 	line = ''
# 	LHArr = []
# 	while line != '---':
# 		line = inputFile.readline()
# 		if line != '\n':
# 			line = line.replace('\n', '')
# 			LHArr.append(line)
# 	del LHArr[len(LHArr)-1]
# 	return LHArr


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

	#print(email)
	#print(regDate)
	#print(lastLogin)
	#print(lastIP)

	inputFile.readline()
	LoginHistory = parseBlock()
	print(LoginHistory)

	skipLines()
	skipLines()


	NameHistory = parseBlock()
	print(NameHistory)

	blockHistory = parseBlock()
	print(blockHistory)

	supportHistory = parseBlock()
	print(supportHistory)

	recoveryHistory = parseBlock()
	print(recoveryHistory)

	print(parseFriends())

	inputFile.readline()

	print(parseMessages())

	

except IOError:
	print("Ошибка работы с файлом!")
finally:
	inputFile.close()

