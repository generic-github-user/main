# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

plt.ion()

# Settings

width = 50
height = 50

# Matrix to store amount of fuel in each cell
fuel = np.zeros([width, height])
for i in range(20):
    fuel[
        int(np.random.uniform(0, width)): int(np.random.uniform(0, width)),
        int(np.random.uniform(0, height)): int(np.random.uniform(0, height))
    ] = np.random.uniform(0.5, 1)

# Store intensity of fire/heat at each cell value
fire = np.zeros([width, height])
fire[width // 2, height // 2] = 1

# Rendered output composed from other two main matrices
render = np.random.uniform(0, 1, [width, height, 3])

fig, ax = plt.subplots()

for u in range(100):
    # for i in range(width):
    #     for j in range(height):
    #         for q in range(width):
    #             for w in range(height):
    #                 data[i, j] += data[q, w] * 0.001

    # Update
    im = ax.imshow(
        fuel,
        interpolation='nearest',
        cmap=cm.plasma,
        origin='lower'
    )
    # Wait until next timestep
    plt.pause(1)
    # Display updated visualization
    plt.show()
