import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

data = np.random.uniform(0, 1, [50, 50])

fig, ax = plt.subplots()
im = ax.imshow(
    data,
    interpolation='nearest',
    cmap=cm.plasma,
    origin='lower'
)

plt.show()
