import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

plt.ion()

width = 50
height = 50
data = np.zeros([width, height])

data[width // 2, height // 2] = 1

fig, ax = plt.subplots()

for u in range(100):
    for i in range(width):
        for j in range(height):
            for q in range(width):
                for w in range(height):
                    data[i, j] += data[q, w] * 0.001

    im = ax.imshow(
        data,
        interpolation='nearest',
        cmap=cm.plasma,
        origin='lower'
    )
    plt.pause(1);
    plt.show()
