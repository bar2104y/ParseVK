import re

#Поиск ссылки на фото
def getPhoto(string):
    link = 'aaa'
    data = re.search(r'([0-9]*)( )(.*?)( \()(.*)(\))',string)
    if data != None:
        link = data.group(5)
    return(link)