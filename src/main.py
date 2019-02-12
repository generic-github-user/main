from PIL import Image
import glob
import tensorflow as tf
tf.enable_eager_execution()

resolution = 32
channels = 4
points = (resolution ** 2) * channels

icons = []
for filename in glob.glob('../data/*.ico'):
      img = Image.open(filename).convert('RGBA')
      img = img.resize((resolution, resolution))
      icons.append(list(sum(list(img.getdata()), ())))

data = tf.constant(icons, dtype=tf.float32)

inputs = tf.keras.Input(shape=(points,))
a = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(inputs)
b = tf.keras.layers.Dense(64, activation=tf.nn.sigmoid)(a)
c = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(b)
outputs = tf.keras.layers.Dense(points)(inputs)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=tf.train.GradientDescentOptimizer(0.00001),
              loss='mean_squared_error',
              metrics=['accuracy'])

model.fit(data, data, epochs=10)
model.evaluate(data, data)
