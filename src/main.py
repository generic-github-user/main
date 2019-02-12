from PIL import Image
import glob
import tensorflow as tf

icons = []
for filename in glob.glob('../data/*.ico'):
      img = Image.open(filename)
      icons.append(img)

inputs = tf.keras.Input(shape=(256,))
a = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(inputs)
b = tf.keras.layers.Dense(64, activation=tf.nn.sigmoid)(a)
c = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(b)
outputs = tf.keras.layers.Dense(256, activation=tf.nn.sigmoid)(c)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
