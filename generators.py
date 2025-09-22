'''
numbers_list = list(range(10000000000)) # error - memory overflow

for i in numbers_list:
    print(i)
'''

'''
class A:
    def __init__(self):
        # return self
        self.state = 1

    def __iter__(self):
        return self

    def __next__(self):
        # return 52 # возникнет бесконечный цикл
        self.state += 1
        return self.state

# for line in map(str.strip, open("input.txt")):
#     print(line)

m = map(str.strip, open("input.txt"))
print(list(m))

# for element in A():
#     print(element)

num = A().__next__()
print(num)
'''

def f():
    print("Reaction")
    yield 1
    print("Hoba!")
    yield 2

for i in f():
    print(i)

def a():
    yield 37
    b = yield 100500
    print(b)

g = a().__iter__()
print(g.__next__())

g.send(100)