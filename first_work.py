'''
#14
from math import *

minn = 10 ** 6
best_u = 0
best_v = 0

for u in range(-100, 100):
    for v in range(-100, 100):
        if 83 * u + 157 * v == 1:
            if abs(u) + abs(v) <= minn:
                minn = abs(u) + abs(v)
                best_u, best_v = u, v

if best_u or best_v:
    print(best_u, best_v, minn)
'''
#18
from math import *

def find(n):
    pairs = []
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            if gcd(a, b) == 1:
                pairs.append((a, b))
    return pairs

n = 50
res = find(n)
print(len(res))