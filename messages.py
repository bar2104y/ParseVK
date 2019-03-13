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
	for message in arr:
		print(message)
		# Разбор информации о сообщении в переменные
		direction = message[0]
		id = re.search(r'(vk.com\/id)(.*)', message[1])
		id = id.group(2)
		tmp = str(message[2]).split(' в ')
		date = tmp[0]
		time = tmp[1]
		message = message[3]

		# перевод данных в html