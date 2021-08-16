import numpy as np
import matplotlib.pyplot as plt
import string
import random


layout = """
1234567890
qwertyuiop[]\\
asdfghjkl;'
zxcvbnm,./
???? ?
"""
layout = list(filter(None, layout.splitlines()))
max_len = len(max(layout, key=len))
layout = [l+('?'*(max_len-len(l))) for l in layout]
layout = list(map(list, layout))
layout = np.array(layout, dtype=str)
print(layout)
