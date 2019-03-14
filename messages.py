import re
# ------------------------------
# -///////--///////////////-----
# -///////----------------------
# -///////--********------------
# -///////---------- *********--
# -///////-------------*******--
# -///////--*****---------------
# -///////--********------------
# ----------************--------
# -------------------*********--

# def parseDialogs():
# def parseURL():

def parseDialogs(name, arr):
# '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <meta charset="utf-8" />
#         <title>''' + name + ''' - друзья</title>
#     </head>
#     <body>
#         <h4>Powered by <a href="https://github.com/bar2104y">bar2104</a> </h4>
#     </body>
# </html>
# '''
	#диалоги
	dialogListAdr = []

	# Составление списка диалогов
	for message in arr:
		if len(message)>1:
			id = re.search(r'(vk.com\/id)(.*)', message[1])
			id = id.group(2)

			f = False
			for i in range(0, len(dialogListAdr)):
				if dialogListAdr[i] == id:
					f = True
					break
			if not f:
				dialogListAdr.append(id)
	
	# Подготовка массива с сообщениями
	dialogListData = []
	for i in range(0, len(dialogListAdr)):
		dialogListData.append([])
	
		

	for message in arr:
		direction = message[0]
		# Костыль
		if len(message)>1:
			id = re.search(r'(vk.com\/id)(.*)', message[1])
			id = id.group(2)
			tmp = str(message[2]).split(' в ')
			date = tmp[0]
			time = tmp[1]
			message = message[3]

			for i in range(0, len(dialogListAdr)):
				if id == dialogListAdr[i]:
					break

			dialogListData[i].append([direction, date,time, message])

	# Оладка 
	for a in dialogListData:
		print(a)
		print()
		print()

	return [dialogListAdr, dialogListData
		
