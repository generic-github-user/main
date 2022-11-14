n = 600851475143
# n = 3252


# probably not a good algorithm; not so bad that I won't be able to live with
# myself
def factorize(x):
    factors = set()
    while x > 1:
        for i in range(2, x+1):
            if x % i == 0:
                factors.add(i)
                x //= i
                break
    return factors


print(factorize(n))
