'''
def create_number(x, y):
    return x + y
print(create_number(10, 20))

def using_star(number_one, number_two, *, number_three):
    return number_one * number_two * number_three
print(using_star(2, 5, number_three=17))

def using_slash(one, two, three, /):
    return one + two + three
print(using_slash(1, 2, 3))

list_words = ["hello", "worlds", "paradise"]
# list_words.sort(key=len)
# print(list_words)
sorted_list = sorted(list_words)
list_words.sort(key=lambda word: word[1])
print(sorted_list)

number_test = 100
print(f"result = {number_test + number_test * 30}")
'''

import re
def get_popular_resource(text):
    pattern = r'GET\s+(\S+) HTTP'
    match = re.search(pattern, text)
    if match:
        recourse = match.group(1)
        return recourse
def get_popular_user(text):
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    match = re.search(pattern, text)
    if match:
        popular_user = match.group()
        return popular_user

with open("log_browser.log") as file:
    texts = str(file.readlines())
    print(get_popular_resource(texts))
    print(get_popular_user(texts))
