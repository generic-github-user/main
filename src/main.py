from PIL import Image
import glob
import tensorflow as tf
from matplotlib import pyplot as plt
import math
tf.enable_eager_execution()


global_step = tf.train.get_or_create_global_step()
summary_writer = tf.contrib.summary.create_file_writer('C:/My Files/Programming/Python/icon-encoder/src/logs', flush_millis=10000)

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

with summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
    inputs = tf.keras.Input(shape=(points,))
    layers = [inputs]
    for i in range(0, int(math.log(points, 8) - 1)):
        nodes = int(points ** (1 / (8 ** i)))
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
    for i in range(1, int(math.log(points, 8) - 2)):
        nodes = int(8 ** i)
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
    outputs = tf.keras.layers.Dense(points)(layers[len(layers)-1])
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
