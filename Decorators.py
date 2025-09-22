'''
mport functools
def decorator(f):
    @functools.wraps(f) # to prevent losing information about the wrapped function
    def modified_f(*args, **kwargs):
        print(f"function called {f.__name__}")
        # print(10)
        return f(*args, **kwargs)
    return modified_f

@decorator
def f():
    print(1)

@decorator
def g():
    print(2)

g = decorator(g)
f()
g()
'''
import functools

'''
import functools

def cache(f):
    cache_dictionary = {}
    @functools.wraps(f)
    def wrapper(*args):
        key = args
        if key not in cache_dictionary:
            cache_dictionary[key] = f(*args)
        return cache_dictionary[key]
    return wrapper

@cache
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)

for i in range(100):
    print(fib(i))
'''

def add(n):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            return result + n
        return wrapper
    return decorator

@add(2)
def f(a, b):
    return a + b

assert f(100, 200) == 302
