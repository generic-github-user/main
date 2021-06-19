# The following code is intended solely for educational and experimental purposes. I do not condone any unethical use of the code and disclaim responsibility from such use.

import ast
import random
import operator as ops

for i in range(2, 50):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i)
