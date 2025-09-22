import re
#
# print(r"qqq\nbbb") # не будет переноса строк
# a = re.findall("a", "bdddsa")
# print(a)
#
# print("aaa\vsss\vqqq")
#
# b = "funny"
# print(re.findall(r'\w', b))

# import unicodedata
#
# # Итерация по всем кодовым точкам Unicode
# for code_point in range(0x110000):
#     try:
#         char = chr(code_point)
#         # Фильтрация непечатаемых символов
#         if unicodedata.category(char)[0] != 'C':
#             print(char, end='')
#     except:
#         pass

# b = re.findall(r': (\w+?)(\w+?)', "What is your name: Ilya")
# print(b)
#
# m = re.search("45", "1612458318")
# print(m)\
