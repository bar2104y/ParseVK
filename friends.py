import re
# Имя пользователя, массив с друзьями
def friendsToHTML(name, arr):
	# arr: [[link,name,surname][link,name,surname]]
	output = '''
	<!DOCTYPE html>
	<html>
	<head>
	<meta charset="utf-8" />
	<title>''' + name + ''' - друзья</title>
	</head>
	<body>
	<h4>Powered by <a href="https://github.com/bar2104y">bar2104</a> </h4>
	<ul>
	'''

	for item in arr:
		print(item[0])
		id = re.search(r'(vk.com\/id)(.*)', item[0])
		id = id.group(2)

		output += '<li><a href="https://vk.com/id' + id +'">' + item[1] + ' ' + item[2] + '</a></li>'


	output += '''
	</ul>
	</body>
	</html>
	'''

	return output