# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

plt.ion()

# Settings

width = 30
height = 30
radius = 7

# Matrix to store amount of fuel in each cell
fuel = np.zeros([width, height])
for i in range(20):
    fuel[
        int(np.random.uniform(0, width)): int(np.random.uniform(0, width)),
        int(np.random.uniform(0, height)): int(np.random.uniform(0, height))
    ] = 1#np.random.uniform(0.5, 1)
fuel_last = np.zeros([width, height])

# Store intensity of fire/heat at each cell value
fire = np.zeros([width, height])
fire[width // 2, height // 2] = 1
fire_last = np.zeros([width, height])

# Rendered output composed from other two main matrices
render = np.random.uniform(0, 1, [width, height, 3])

fig, ax = plt.subplots()

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

for u in range(100):
    np.copyto(fuel_last, fuel)
    np.copyto(fire_last, fire)

    for i in range(width):
        for j in range(height):
            for q in range(i - (radius // 2), i + (radius // 2)):
                for w in range(j - (radius // 2), j + (radius // 2)):
                    x = np.clip(q, 0, width-1)
                    y = np.clip(w, 0, height-1)

                    if [i, j] != [x, y]:
                        fire[i, j] += fuel_last[x, y] * fire_last[x, y] / distance(i, j, x, y)

                    fire[i, j] *= fuel[i, j]

    # Update
    im = ax.imshow(
        fire,
        interpolation='nearest',
        cmap=cm.plasma,
        origin='lower'
    )
    # Wait until next timestep
    plt.pause(1)
    # Display updated visualization
    plt.show()
