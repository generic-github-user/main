from lib.pyiter import range

print(range(1, 10).to_string())
range(1, 10).print()

print(range(1, 10).to_list())
print(range(1, 10).to_set())
print(range(1, 10).inner)
print(range(1, 10).all(lambda x: x < 20))
# range(1, 20).next().print()
range(-10, 11).map(lambda x: x ** 2).print()
# range(32, 42).filter(lambda _: True).print()

# range(2, 3000).filter(lambda x:
    # range(2, ceil(x**0.5)+1)
    # .all(lambda y: x % y != 0 or x == y)).print()
# .nth(100)
