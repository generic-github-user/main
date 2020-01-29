import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

width = 50
height = 50
data = np.zeros([width, height])

data[width // 2, height // 2] = 1

fig, ax = plt.subplots()
im = ax.imshow(
    data,
    interpolation='nearest',
    cmap=cm.plasma,
    origin='lower'
)

plt.show()
