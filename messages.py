import re
from attachments import getPhoto

def attachmentsType(inputtext):
	#photo audio wall video sticker doc gift link
	at = re.search(r'([0-9]*)( )(.*?)( )(.*\))', inputtext)
	at = at.group(3) if at != None else 'Error'
	return(at)


# форматирование вложения
def parseAttachments(mesAttachments):
	string = mesAttachments

	aType = attachmentsType(string)
	
	#Костыль вместо switch case
	if aType == 'photo':
		link = getPhoto(string)
		tmp = '<a src="' + link + '"><img src = "' + link + '"></a>'
	else:
		tmp = 'Вложение ' + aType + '<br>'
	return(tmp)
	


def parseDialogs(name, arr):
	#диалоги
	#arr - все сообщения(вообще все)
	dialogListAdr = []
	print('Разбор диалогов')

	# Составление списка диалогов
	for message in arr:
		# Костыль для отсеивания сообщений из чатов(не личных)
		if len(message) >= 3:
			# Получение id собеседника
			id = re.search(r'(vk.com\/id)(.*)', message[1])
			if id != None:
				id = id.group(2)

				# определяет уникальность собеседника
				# Если встречается первый раз - записываем, иначе - игнорируем
				f = False
				for i in range(0, len(dialogListAdr)):
					if dialogListAdr[i] == id:
						f = True
						break
				if not f:
					dialogListAdr.append(id)
	
	# Подготовка массива с сообщениями
	# Создание структуры массива
	dialogListData = []
	for i in range(len(dialogListAdr)):
		dialogListData.append([])

	#перебор сообщений, распределение по диалогам
	'''
	message : [1, 'https://vk.com/id12565', '13.10.2015 в 17:49:21', 'не хочу об этом говорить']

	'''
	for message in arr:
		
		if len(message) >= 3:
			direction = message[0]
			id = re.search(r'(vk.com\/id)(.*)', message[1])
			id = id.group(2)
			tmp = str(message[2]).split(' в ')
			date = tmp[0]
			time = tmp[1]
			message = message[3]
			message = re.sub(r'Кому:', ' ', message)
			message = re.sub(r'От кого:', ' ', message)

			attachments = re.findall(r'(Прикрепление #.*)', message)
			
			if len(attachments) > 0:
				for at in attachments:
					at = re.split(r'(Прикрепление #)', at)
					for a in at:
						if a != 'Прикрепление #' and a != '':
							message += '<br> ' + parseAttachments(a)
			message = re.sub(r'(Прикрепление #[0-9]*)( )(.*?)( )(.*\))', ' ', message)
			print(date,time, message)
					
			


			for i in range(0, len(dialogListAdr)):
				if id == dialogListAdr[i]:
					break

			# Добавление сообщения в массив
			dialogListData[i].append([direction, date,time, message])

	# Список id людей, массив с сообщениями
	return dialogListAdr, dialogListData