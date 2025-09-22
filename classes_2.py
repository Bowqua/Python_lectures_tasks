"""
class A:
    w = 42

class B(A):
    ww = 444

    def __init__(self):
        print("Hello")

class C(B, A):
    number = 37

    def __init__(self):
        super().__init__()
        print("Bye")

print(C.__mro__) # (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)

a = A()
print(a.w)
print(B.w)
print(B.ww)
print(C.ww)

r = B()
print(r.w, "- from r")

d = C()
print(d.w, "- from d")
"""

'''
def f_errors(number):
    try:
        5 / number
    except ZeroDivisionError:
        print("Division by zero")

f_errors(0)
'''
import sys
import math as m
import numpy as np

def f0():
    10 / 0

def f1():
    10 / "hello"

def f2():
    10 / 0

def f3():
    print(np.float64(1.0) / np.float64(0.0))

def f4():
    try:
        m.exp(1000)
        raise OverflowError("exp() argument too large")
    except OverflowError:
        print("OverflowError caught")

def f5():
    1 / 0

def f6():
    10 / 0

def f7():
    m = "my"
    my = my.noattr
    print(my)

def f8():
    with open('nonexistent_file.txt', 'r') as file:
        data = file.read()

def f9():
    import mathhh as m

def f10():
    m = [1, 1, 1]
    print(m[10])

def f11():
    text = "hello"
    print(text[100])

def f12():
    dict = { "cat" : "Mine", "dog": "John" }
    try:
        print(dict["horse"])
    except KeyError:
        print("KeyError caught")

def f13():
    input = input()
    print(inputtt)

def f14():
    try:
        print("hello!")
    except SyntaxError:
        print("SyntaxError")
def f15():
    try:
        m.sqrt(-10)
    except ValueError:
        print("ValueError caught")

def f16():
    byte_data = b'\x80\x81\x82'
    decoded_text = byte_data.decode('utf-8')
    print(decoded_text)

def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)

check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")

