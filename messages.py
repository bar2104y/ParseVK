import re

def parseAttachments(mesAttachments):
	string = ''
	for a in mesAttachments:
		string += str(a)
	atInfo = re.search(r'(Прикрепление #)([0-9]*)( )(.*)?( )(.*)', string)
	print(atInfo)
	print(string)
	print()


def parseDialogs(name, arr):
	#диалоги
	dialogListAdr = []

	# Составление списка диалогов
	for message in arr:
		# Костыль для отсеивания сообщений из чатов(не личных)
		if len(message)>1:
			# Получение id собеседника
			id = re.search(r'(vk.com\/id)(.*)', message[1])
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
	for i in range(0, len(dialogListAdr)):
		dialogListData.append([])

	for message in arr:
		direction = message[0]
		# Костыль, отсеивающий сообщения из чатов
		# Надеюсь исправить потом
		if len(message)>1:
			id = re.search(r'(vk.com\/id)(.*)', message[1])
			id = id.group(2)
			tmp = str(message[2]).split(' в ')
			date = tmp[0]
			time = tmp[1]
			message = message[3]
			
			attachments = re.findall(r'(Прикрепление #)(.*\))',message)
			if len(attachments) > 0:
				for at in attachments:
					parseAttachments(at)
				#print(attachments)


			for i in range(0, len(dialogListAdr)):
				if id == dialogListAdr[i]:
					break

			# Добавление сообщения в массив
			dialogListData[i].append([direction, date,time, message])

	# Список id людей, массив с сообщениями
	return dialogListAdr, dialogListData