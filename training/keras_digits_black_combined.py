#!/usr/bin/python3

print('')
print('=======================================================================')
print('')
print('This script trains a neural network to recognize handwritten digits')
print(' the testing set is concatenated onto the training set to improve accuracy')
print('')

from keras.datasets import mnist
import numpy as np

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

from keras import models
from keras import layers
network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))

network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

train_images = train_images.reshape((60000, 28 * 28))
print('shape of train_images: ', train_images.shape)

test_images = test_images.reshape((10000, 28 * 28))
print('shape of test_images: ', test_images.shape)

print('Concatenating train_images and test_images...')
train_images = np.concatenate((test_images, train_images), axis=0)
train_labels = np.concatenate((test_labels, train_labels), axis=0)
print('new shape of train_images: ', train_images.shape)

print('Converting all images to black and white...')
train_images = np.where(train_images > 80, 255, 0)
train_images = train_images.astype('float32') / 255
print('done.')

print('debug images data: ')    # DEBUG
print(train_images[0])          # DEBUG

from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

print('')
print('training model...')
network.fit(train_images, train_labels, epochs=10, batch_size=128)
print('done.')

print('Saving model...')
network.save('kerasModel.model', save_format='h5')
print('done.')


