from PIL import Image
import glob
import tensorflow as tf
from matplotlib import pyplot as plt
tf.enable_eager_execution()

resolution = 32
channels = 4
points = (resolution ** 2) * channels
epochs = 1000
optimizer = tf.train.AdamOptimizer(0.01)
delay = 0.1

icons = []
for filename in glob.glob('../data/*.ico'):
      img = Image.open(filename).convert('RGBA')
      img = img.resize((resolution, resolution))
      icons.append(list(sum(list(img.getdata()), ())))

data = tf.constant(icons, dtype=tf.float32)

inputs = tf.keras.Input(shape=(points,))
a = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(inputs)
b = tf.keras.layers.Dense(64, activation=tf.nn.sigmoid)(a)
c = tf.keras.layers.Dense(2, activation=tf.nn.sigmoid)(b)
d = tf.keras.layers.Dense(64, activation=tf.nn.sigmoid)(c)
e = tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)(d)
outputs = tf.keras.layers.Dense(points)(e)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=optimizer,
              loss='mean_squared_error',
              metrics=['accuracy'])

plot = plt.imshow(tf.zeros([resolution, resolution, channels]), interpolation='nearest')
plt.ion()
plt.show()
class Render(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        image = tf.slice(data, tf.constant([0, 0]), tf.constant([1, points]))
        prediction = tf.cast(tf.reshape(model(image), [resolution, resolution, channels]), tf.int32)
        plot.set_data(prediction)
        plt.draw()
        plt.pause(delay)

callback = Render()

model.fit(data, data, epochs=epochs, callbacks=[callback])
model.evaluate(data, data)

print('Press enter to exit the program.')
input()
