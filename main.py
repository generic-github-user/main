import numpy as np
import matplotlib.pyplot as plt

canvas = np.zeros([300, 600])
plt.imshow(canvas)
plt.show()
outlines = {
    # 'a': ['left', 'down']
    'a': 'ur,u,l,dl,d,r,ur,dr'
}
