# Import libraries
from PIL import Image
import glob
import tensorflow as tf
from matplotlib import pyplot as plt
import math
# Enable eager execution to allow imperative calls to the TensorFlow API
tf.enable_eager_execution()

# Set up TensorBoard
global_step = tf.train.get_or_create_global_step()
summary_writer = tf.contrib.summary.create_file_writer('C:/My Files/Programming/Python/icon-encoder/src/logs', flush_millis=10000)

# Settings
resolution = 32
channels = 4
points = (resolution ** 2) * channels
epochs = 200
loss = tf.losses.mean_squared_error
optimizer = tf.train.AdamOptimizer(learning_rate=0.0001)
delay = 0.1
layer_ratio = 2
shallowness = 3

# Load image data
print('Loading images for training . . .')
icons = []
for filename in glob.glob('../data/*.ico'):
      # Attempt to load image and add its data to icons list
      try:
          img = Image.open(filename).convert('RGBA')
          img = img.resize((resolution, resolution))
          icons.append(list(sum(list(img.getdata()), ())))
      # Print error message if image cannot be loaded
      except:
          print(filename + ' could not be loaded due to an error.')

# Convert array of pixel data to TensorFlow tensor
data = tf.constant(icons, dtype=tf.float32)
dataset = tf.data.Dataset.from_tensor_slices(data).repeat().batch(32)
iter = dataset.make_one_shot_iterator()
# Don't use x as a variable name
batch = iter.get_next()

def random_average(a, b):
    # c = tf.random_uniform([1])
    c = tf.random_uniform(a.shape)
    return (a * c) + (b * (1 - c))

with summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
    # Create autoencoder model
    encoder_inputs = tf.keras.Input(shape=(points,))
    layers = [encoder_inputs]
    print('Generating model layer structure:')
    num_layers = int(math.log(points, layer_ratio))
    for i in range(0, num_layers - 2 - shallowness):
        nodes = int(points * (0.5 ** (i + 1)))
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.relu)(layers[i])
        layers.append(new_layer)
        print(nodes)
    encoder = tf.keras.Model(inputs=encoder_inputs, outputs=layers[len(layers)-1])

    decoder_inputs = tf.keras.Input(shape=(nodes,))
    layers = [decoder_inputs]
    for i in range(0, num_layers - shallowness - 1):
        nodes = int(layer_ratio ** (i + 1 + shallowness))
        new_layer = tf.keras.layers.Dense(nodes, activation=tf.nn.relu)(layers[i])
        layers.append(new_layer)
        print(nodes)
    decoder_outputs = tf.keras.layers.Dense(points)(layers[len(layers)-1])
    decoder = tf.keras.Model(inputs=decoder_inputs, outputs=decoder_outputs)

    # autoencoder = tf.keras.Model(inputs=encoder_inputs, outputs=decoder_outputs)

    def autoencode(inputs):
        return decoder(encoder(inputs))

    def calc_loss():
        loss_value = loss(autoencode(batch), batch)
        print(loss_value)
        return loss_value

    print('Model generated.')

    # f = plt.figure()
    f, axarr = plt.subplots(2, 2)
    # Prepare matplotlib plot for rendering outputs
    # plot = f.add_subplot(1,2, 1)
    plot = axarr[0,0].imshow(tf.zeros([resolution, resolution, channels]), interpolation='nearest')
    # reconstructions = f.add_subplot(1,2, 2)
    reconstructions = axarr[0,1].imshow(tf.zeros([resolution * 10, resolution * 10, channels]), interpolation='nearest')

    random_generated = axarr[1,0].imshow(tf.zeros([resolution, resolution, channels]), interpolation='nearest')
    random_generated_set = axarr[1,1].imshow(tf.zeros([resolution * 10, resolution * 10, channels]), interpolation='nearest')

    # Enter interactive plotting mode so that plots can be updated while training without stopping the program flow
    plt.ion()
    # Don't use block=True
    plt.show()
    # Render various data visualizations after each training epoch ends
    def on_epoch_end():
        # Slice one image from the training data tensor
        image = tf.slice(data, tf.constant([0, 0]), tf.constant([1, points]))
        # Run prediction (compression and reconstruction) with model
        prediction = tf.cast(tf.reshape(autoencode(image), [resolution, resolution, channels]), tf.int32)
        # Update plot with newly generated result
        plot.set_data(tf.clip_by_value(prediction, 0, 255))

        images = tf.slice(data, tf.constant([0, 0]), tf.constant([100, points]))
        predictions = tf.cast(tf.squeeze(tf.contrib.gan.eval.image_grid(autoencode(images), [10, 10], [resolution, resolution], channels)), tf.int32)
        reconstructions.set_data(tf.clip_by_value(predictions, 0, 255))

        images = tf.slice(data, tf.constant([0, 0]), tf.constant([100, points]))
        compressed = encoder(images)
        min = tf.reduce_min(compressed, axis=0)
        max = tf.reduce_max(compressed, axis=0)

        # random_sample = tf.expand_dims(random_average(min, max), axis=0)
        # random_sample = tf.random_uniform([1, 16]) * 10
        weights = tf.random_uniform([100, 1])
        random_sample = tf.expand_dims(tf.reduce_sum(compressed * (weights / tf.reduce_sum(weights)), axis=0), axis=0)
        print(random_sample)
        generated = tf.reshape(decoder(random_sample), [resolution, resolution, channels])
        random_generated.set_data(tf.clip_by_value(generated, 0, 255))

        plt.draw()
        plt.pause(delay)

    print('Training model . . .')
    for i in range(epochs):
        optimizer.minimize(calc_loss)
        on_epoch_end()
    print('Model training complete.')

# Wait for user input to close program
print('Press enter to exit the program.')
input()
