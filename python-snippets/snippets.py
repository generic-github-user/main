#!/usr/bin/env python
# coding: utf-8

# ### Prime Number Generator
# Prints out a list of prime numbers in the specified range.

for i in range(2, 50):
    for j in range(2, round(i**(1/2))):
        if i % j == 0:
            break
    else:
        print(i)


# ### Flatten Nested List
# Convert an irregular ordered list of lists and/or values to a shallow sequence of values.
# Source: https://stackoverflow.com/a/14491059/10940584

def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item

list(flatten([[[1, 2, 3], [4, 5]], 6]))


# ## String Manipulation


def makelist(items):
    return ', '.join(items[:-1])+', and '+items[-1]

makelist(list('xyz'))


values = [
    [100, '$100 bill'],
    [50, '$50 bill'],
    [20, '$20 bill'],
    [10, '$10 bill'],
    [5, '$5 bill'],
    [1, '$1 bill'],
    [0.25, 'quarter'],
    [0.10, 'dime'],
    [0.05, 'nickel'],
    [0.01, 'penny']
]
nums, labels = list(zip(*values))
c = subdivide(12.34, nums)
print(nums)
makelist(['{} x {}'.format(int(b[1]), labels[nums.index(b[0])]) for b in c])
makelist([plural(labels[nums.index(b[0])], int(b[1]), True) for b in c])


def change(amount):
    c = subdivide(amount, nums)
    return makelist([plural(labels[nums.index(b[0])], int(b[1]), True) for b in c])

print(change(378.22))
# TODO: flood fill

