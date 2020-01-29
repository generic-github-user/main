# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

plt.ion()

# Settings

width = 20
height = 20
radius = 5
fuel_decay = 0.01
# fire_decay = 0
iterations = 100
delay = 1
spreading_factor = 0.01
noise = 10

# Matrix to store amount of fuel in each cell
fuel = np.zeros([width, height])
for i in range(20):
    # Generate some random fuel blocks
    fuel[
        # Slice from one random coordinate on the screen to another
        int(np.random.uniform(0, width)): int(np.random.uniform(0, width)),
        int(np.random.uniform(0, height)): int(np.random.uniform(0, height))
    ] = np.random.uniform(0.5, 1)
# Variable to store previous state of simulation
fuel_last = np.zeros([width, height])

# Store intensity of fire/heat at each cell value
fire = np.zeros([width, height])
fire[width // 2, height // 2] = 1
fire_last = np.zeros([width, height])

# Rendered output composed from other two main matrices
render = np.random.uniform(0, 1, [width, height, 3])

fig, ax = plt.subplots(1, 3)

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

for u in range(iterations):
    # TODO: check that copying is working correctly
    np.copyto(fuel_last, fuel)
    np.copyto(fire_last, fire)

    # Loop through all cells on screen
    for i in range(width):
        for j in range(height):
            # Loop through neighboring cells according to radius setting
            for q in range(i - (radius // 2), i + (radius // 2)):
                for w in range(j - (radius // 2), j + (radius // 2)):
                    # Limit coordinates to positions on grid
                    x = np.clip(q, 0, width-1)
                    y = np.clip(w, 0, height-1)

                    # Don't use the current cell when evaluating fire for next timestep
                    if [i, j] != [x, y]:
                        # Update heat/fire intensity
                        fire[i, j] += fuel_last[x, y] * fire_last[x, y] * spreading_factor * np.random.uniform(1, 1+noise) / distance(i, j, x, y)

                    # Reduce amount of fuel in cell by decay rate by fire intensity, with random noise factored in. Clip to [0, 1]
                    fuel[i, j] = np.clip(fuel[i, j] - (fuel_decay * fire_last[i, j] * np.random.uniform(1, 1+noise)), 0, 1)
            # Multiply current fire intensity by fuel amount in cell
            fire[i, j] *= fuel[i, j]
            fire[i, j] = np.clip(fire[i, j], 0, 1)

    # Update
    im = ax[0].imshow(
        fuel,
        interpolation='nearest',
        cmap=cm.plasma,
        origin='lower'
    )
    im2 = ax[1].imshow(
        fire,
        interpolation='nearest',
        cmap=cm.plasma,
        origin='lower'
    )
    # Wait until next timestep
    plt.pause(delay)
    # Display updated visualization
    plt.show()
