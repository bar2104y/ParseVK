import re
from pprint import pprint
from friends import friendsToHTML
from messages import parseDialogs

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


# Перевод непустых строк в элементы массива до конца блока(---)
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
	return Arr
		

path = 'log.txt'
try:
	# Разбор первой строки
	inputFile = open(path, 'r')
	line = inputFile.readline()
	vkID = re.search(r'(vk.com\/id)(.*?)( \()', line)
	vkID = vkID.group(2)

	tmp = re.findall(r'(\()(.*?)(\))', line)

	personalLink = tmp[0][1]
	name = str(tmp[1][1])

	# Общая информация
	email = searchOnce('(Email: )(.*)')
	regDate = searchOnce('(Регистрация: )(.*)')
	lastLogin = searchOnce('(Последнее посещение: )(.*)')
	lastIP = searchOnce('(IP-адрес последнего посещения: )(.*)')
	phone = searchOnce('(Телефон: )(.*)')

	# Костыль
	inputFile.readline()
	# История авторизации
	LoginHistory = parseBlock()

	# Костыли
	skipLines()
	skipLines()

	# парсинг в массивы
	nameHistory = parseBlock()
	del nameHistory[0]
	blockHistory = parseBlock()

	supportHistory = parseBlock()
	del supportHistory[0]
	
	recoveryHistory = parseBlock()

	friends = parseFriends()

	# Костыль
	inputFile.readline()

	# Массив с сообщениями
	# [[direction(0 in; 1 out), userlink, date, message],
	#  [direction(0 in; 1 out), userlink, date, message]]
	messages = parseMessages()

	# Разбор информации

	html = '''
	<!DOCTYPE html>
	<html>
	<head>
	<meta charset="utf-8" />
	<title>''' + name + ''' - данные пользователя</title>
	</head>
	<body>
	<h4>Powered by <a href="https://github.com/bar2104y">bar2104</a> </h4>
	<p>Данные пользователя <a href = "https://vk.com/id''' + vkID +'''">''' + name + '''</a></p>
	<ul>
		<li>ВК ID:               ''' + vkID + '''</li>
		<li>Почта:               ''' + email + '''</li>
		<li>Телефон:             +''' + phone + '''</li>
		<li>Дата регистрации:    ''' + regDate + '''</li>
		<li>Последнее посещение: ''' + lastLogin + '''</li>
		<li>Последний IP:        ''' + lastIP + '''</li>
	</ul>

	<p>Полезное:</p>
	<ul>
		<li><a href="friends.html">Список друзей</a></li>
		<li><a href="messages.html">Сообщения</a></li>
	</ul>

	<p>История последних посещений (информация актуальна на момент получения файла)</p>
	<ul>
	'''

	for l in LoginHistory:
		html += '<li>' + l + '</li>'
	html += '</ul>'

	html += '<p>История обращений в техническую поддержку</p><ul>'
	for shi in supportHistory:
		shit = shi.split(':')
		html += '<li>' + shit[1] + ':' + shit[2] + ' -- ' + shit[0][2:] + '</li>'
	html += '</ul>'

	del shi, shit

	html += '<p>История смены имен</p><ul>'
	for nhi in reversed(nameHistory):
		tmp = nhi.split(': ')
		time = tmp[0]
		tmp = tmp[1].split(" --> ")
		html += '<li>' + time + ' : ' + tmp[0] + ' ==> ' + tmp[1] + '</li>'
	html += '</ul>'
	
	
	html += '''
	</body>
	</html>
	'''

	# Создание html со списком друзей
	friendsHTML = friendsToHTML(name, friends)

	friendsFile = open('friends.html', 'w')
	friendsFile.write(friendsHTML)
	friendsFile.close()

	outputFile = open('index.html', 'w')
	outputFile.write(html)
	outputFile.close()

	parseDialogs(name, messages)

except IOError:
	print("Ошибка работы с файлом!")
finally:
	inputFile.close()
	print('Работа завершена')