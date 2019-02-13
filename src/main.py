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
layer_ratio = 2

print('Loading images for training . . .')
icons = []
for filename in glob.glob('../data/*.ico'):
      try:
          img = Image.open(filename).convert('RGBA')
          img = img.resize((resolution, resolution))
          icons.append(list(sum(list(img.getdata()), ())))
      except:
          print(filename + ' could not be loaded due to an error.')

data = tf.constant(icons, dtype=tf.float32)

with summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
    inputs = tf.keras.Input(shape=(points,))
    layers = [inputs]
    print('Generating model layer structure:')
    num_layers = int(math.log(points, layer_ratio)
    for i in range(0, num_layers - 2)):
        nodes = int(points * (0.5 ** (i + 1)))
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
        print(nodes)
    for i in range(1, num_layers):
        nodes = int(layer_ratio ** i)
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
        print(nodes)
    outputs = tf.keras.layers.Dense(points)(layers[len(layers)-1])
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    print('Model generated.')

    print('Compiling model for training . . .')
    model.compile(optimizer=optimizer,
                  loss='mean_squared_error',
                  metrics=['accuracy'])
    print('Model successfully compiled.')

    plot = plt.imshow(tf.zeros([resolution, resolution, channels]), interpolation='nearest')
    plt.ion()
    plt.show()
    class Render(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            image = tf.slice(data, tf.constant([0, 0]), tf.constant([1, points]))
            prediction = tf.cast(tf.reshape(model(image), [resolution, resolution, channels]), tf.int32)
            plot.set_data(tf.clip_by_value(prediction, 0, 255))
            plt.draw()
            plt.pause(delay)

    callback = Render()

    print('Training model . . .')
    model.fit(data, data, epochs=epochs, callbacks=[callback])
    model.evaluate(data, data)
    print('Model training complete.')

print('Press enter to exit the program.')
input()
