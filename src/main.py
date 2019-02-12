from PIL import Image
import glob
import tensorflow as tf
tf.enable_eager_execution()

icons = []
for filename in glob.glob('../data/*.ico'):
      img = Image.open(filename).convert('RGBA')
      img = img.resize((32, 32))
      icons.append(list(sum(list(img.getdata()), ())))

data = tf.constant(icons, dtype=tf.float32)

inputs = tf.keras.Input(shape=(4096,))
a = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(inputs)
b = tf.keras.layers.Dense(64, activation=tf.nn.sigmoid)(a)
c = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(b)
outputs = tf.keras.layers.Dense(4096, activation=tf.nn.sigmoid)(c)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
