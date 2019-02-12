from PIL import Image
import glob

icons = []
for filename in glob.glob('../data/*.ico'):
      img = Image.open(filename)
      icons.append(img)
