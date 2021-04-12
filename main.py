import numpy as np
import matplotlib.pyplot as plt

canvas = np.zeros([300, 600])
plt.imshow(canvas)
plt.show()
outlines = {
    # 'a': ['left', 'down']
    'a': 'ur,u,l,dl,d,r,ur,dr'
}

coords = {
    'u': npa([0, 1]),
    'd': npa([0, -1]),
    'r': npa([1, 0]),
    'l': npa([-1, 0]),
    'm': npa([-1, 0]),
}
