import itertools
def fib():
    z = [1]
    while True:
        z.append(sum(z[-2:]))
        if len(z) > 2: z.pop(0)
        yield z[-1]

print(sum(filter(lambda x: x % 2 == 0,
           itertools.takewhile(lambda y: y <= 4e6, fib()))))
