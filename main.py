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
	print('Парсинг сообщений')
	global vkID
	line = ''
	stopString = 'Сообщения, оставленные на стене пользователя https://vk.com/id'+vkID+':\n'
	
	Arr = []
	flag = False
	#Читаем диалог пока не вылезет флаг или следующий раздел
	while line != 'От кого:\n' and line != 'Кому:\n' and line != stopString:
		line = inputFile.readline()
	while line != stopString and not flag:
		# message info 
		# [direction(0 in; 1 out), userlink, date, message]
		tmp = []
		if line == 'От кого:\n':
			tmp.append(0)
		else:
			tmp.append(1)

		#В этой строке Пользователь
		line = inputFile.readline()
		#Вычленение информации о пользователе(кому/от кого сообщение)
		if re.findall(r'Пользователь',line) != []:
			isUser = True
			userlink = re.search(r'(https://vk.com/id)(.*)?', line)
			userlink = str(userlink.group()).replace(')', '')
			tmp.append(userlink)
			dbg = str(inputFile.readline()).replace('\n', '')
			tmp.append(dbg)
		else:
			isUser = False

		mes = ''
		while line != 'От кого:\n' and line != 'Кому:\n':
			line = inputFile.readline()
			if line == stopString:
				#Если другой раздел, то уходим домой
				flag = True
				tmp.append(mes.replace('\n', ' '))
				Arr.append(tmp)
				return Arr
			mes += line
		
		tmp.append(mes.replace('\n', ' '))
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

	messagesArd, messagesList = parseDialogs(name, messages)

	print(messagesArd)
	# На каждого пльзователя своя страница.
	# Название файла - id собеседника
	# Сообщения оборачиваются в HTML каркас
	for i in range(0, len(messagesArd)):
		filename = str(messagesArd[i]) + '.html'
		htmlMessage = '<link rel="stylesheet" href="stylesheet.css">'
		for message in messagesList[i]:
			
			# Если сообщения входящее, то отображается слева
			# Если исходящее - справа
			if message[0] == 1:
				direction = "mes_dir_out"
			else:
				direction = "mes_dir_in"
			
			# Бессмысленно, но я так хочу
			date = message[1]
			time = message[2]
			text = message[3]

			htmlMessage += '<div id="' + direction + '''">
			<p class="mes_time">''' + date + ' ' + time + '''</p>
			<p class="mes_text">''' + text + '</p></div><hr>\n'''
		# Запись файла
		try:
			f = open(filename, 'w')
			f.write(htmlMessage)
			
		except IOError:
			print("Ошибка записи диалога")
		finally:
			# Сообщение в консоль
			f.close()
			print('Файл', filename, 'успешно записан')

	mesListHtml = "<ul>"
	for id in messagesArd:
		mesListHtml += '<li><a href="'+id+'.html">' + id + '</a></li>'
	mesListHtml += "</ul>"

	f = open("messages.html", 'w')
	f.write(mesListHtml)
	f.close()
	print('Файл со списком диалогов создан')

except IOError:
	print("Ошибка работы с файлом!")
finally:
	inputFile.close()
	print('Работа завершена')