from PIL import Image, ImageDraw
import sys
import matplotlib.pyplot as plt
import numpy as np
import copy
# with Image.open("hopper.jpg") as im:

canvas_size = np.array([100]*2)
n, m = canvas_size
im = Image.new('RGB', (n, m), (255, 255, 255))

draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)

# write to stdout
# im.save(sys.stdout, "PNG")
# im.show()
