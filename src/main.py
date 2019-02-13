# Import libraries
from PIL import Image
import glob
import tensorflow as tf
from matplotlib import pyplot as plt
import math
tf.enable_eager_execution()

# Set up TensorBoard
global_step = tf.train.get_or_create_global_step()
summary_writer = tf.contrib.summary.create_file_writer('C:/My Files/Programming/Python/icon-encoder/src/logs', flush_millis=10000)

# Settings
resolution = 32
channels = 4
points = (resolution ** 2) * channels
epochs = 1000
optimizer = tf.train.AdamOptimizer(0.01)
delay = 0.1
layer_ratio = 2
shallowness = 3

# Load image data
print('Loading images for training . . .')
icons = []
for filename in glob.glob('../data/*.ico'):
      try:
          img = Image.open(filename).convert('RGBA')
          img = img.resize((resolution, resolution))
          icons.append(list(sum(list(img.getdata()), ())))
      except:
          print(filename + ' could not be loaded due to an error.')

# Convert array of pixel data to TensorFlow tensor
data = tf.constant(icons, dtype=tf.float32)

with summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
    # Create autoencoder model
    inputs = tf.keras.Input(shape=(points,))
    layers = [inputs]
    print('Generating model layer structure:')
    num_layers = int(math.log(points, layer_ratio))
    for i in range(0, num_layers - 2 - shallowness):
        nodes = int(points * (0.5 ** (i + 1)))
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
        print(nodes)
    for i in range(1 + shallowness, num_layers):
        nodes = int(layer_ratio ** i)
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.sigmoid)(layers[i])
        layers.append(new_layer)
        print(nodes)
    outputs = tf.keras.layers.Dense(points)(layers[len(layers)-1])
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    print('Model generated.')

    # Compile model
    print('Compiling model for training . . .')
    model.compile(optimizer=optimizer,
                  loss='mean_squared_error',
                  metrics=['accuracy'])
    print('Model successfully compiled.')

    # f = plt.figure()
    f, axarr = plt.subplots(2, 2)
    # Prepare matplotlib plot for rendering outputs
    # plot = f.add_subplot(1,2, 1)
    plot = axarr[0,0].imshow(tf.zeros([resolution, resolution, channels]), interpolation='nearest')
    # reconstructions = f.add_subplot(1,2, 2)
    reconstructions = axarr[0,1].imshow(tf.zeros([resolution * 10, resolution * 10, channels]), interpolation='nearest')

    x = axarr[1,0].imshow(tf.zeros([resolution * 10, resolution * 10, channels]), interpolation='nearest')
    y = axarr[1,1].imshow(tf.zeros([resolution * 10, resolution * 10, channels]), interpolation='nearest')

    plt.ion()
    # Don't use block=True
    plt.show()
    class Render(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            # Slice one image from the training data tensor
            image = tf.slice(data, tf.constant([0, 0]), tf.constant([1, points]))
            # Run prediction (compression and reconstruction) with model
            prediction = tf.cast(tf.reshape(model(image), [resolution, resolution, channels]), tf.int32)
            # Update plot with newly generated result
            plot.set_data(tf.clip_by_value(prediction, 0, 255))

            images = tf.slice(data, tf.constant([0, 0]), tf.constant([100, points]))
            predictions = tf.cast(tf.squeeze(tf.contrib.gan.eval.image_grid(model(images), [10, 10], [resolution, resolution], channels)), tf.int32)
            reconstructions.set_data(tf.clip_by_value(predictions, 0, 255))

            plt.draw()
            plt.pause(delay)

    callback = Render()

    print('Training model . . .')
    model.fit(data, data, epochs=epochs, callbacks=[callback])
    model.evaluate(data, data)
    print('Model training complete.')

print('Press enter to exit the program.')
input()
