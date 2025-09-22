import os
import signal
import threading
import time

"""
def handler(s, s2):
    print("handling signal", s, s2)

signal.signal(15, handler)

while True:
    pass
"""

"""
os.fork()
os.fork()
os.fork() #выведутся Hello 8 раз, разделение процессов
print("Hello")

while True:
    os.fork() #нельзя запускать! Это форк-бомба, компьютер сломается
"""

# def t(start, end):
#     s = 0
#     for i in range(start, end):
#         s += i
#
#     print(s)
#
# threads = threading.Thread(target=t, args=(0, 10_000_000)) #запускаем поток
# threads.start()

sum = 0
lock = threading.Lock()
def t(number):
    global sum

    with lock:
        for i in range(0, number):
            sum += number
            print(f"current sum: {sum}")

thread_1 = threading.Thread(target=t, args=(10,))
thread_2 = threading.Thread(target=t, args=(15,))
thread_1.start()
thread_2.start()
