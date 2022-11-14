# from lib.streams import range
from lib.wrapstreams import range
import math

# import sys
# sys.setrecursionlimit(30000)

# range(1, 10e9).filter(lambda x: x % 5 == 0)
R = 10e6
range(-R, R+1).map(lambda x: x ** 2)

print(range(1, 10).to_string())
range(1, 10).print()

print(range(1, 10).to_list())
print(range(1, 10).to_set())
print(range(1, 10).all(lambda x: x < 20))
range(-10, 11).map(lambda x: x ** 2).print()
range(1, 42).filter(lambda x: x % 3 == 0).print()
# range(1, 2000).filter(lambda x: math.sqrt(x) % 1 == 0).print()

is_prime = lambda x: range(2, math.ceil(x**0.5)+1)\
                  .all(lambda y: x % y != 0 or x == y)
range(2, 100).filter(is_prime).print()
print(range(2, 10e8).filter(is_prime).nth(10000))
