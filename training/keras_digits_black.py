#!/usr/bin/python3

print('')
print('=======================================================================')
print('')
print('This script trains a neural network to recognize handwritten digits')
print(' and then tests the network with a set of test images.')
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

train_images = np.where(train_images > 80, 255, 0)
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = np.where(test_images > 80, 255, 0)
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

from keras.utils import to_categorical
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

print('')
print('training...')
print('')

network.fit(train_images, train_labels, epochs=10, batch_size=128)

print('')
print('testing...')
print('')

test_loss, test_acc = network.evaluate(test_images, test_labels)

print('')
#print('test accuracy:', test_acc)
print('')

# now do noah's test

print('shape of test_images: ', test_images.shape)

first = test_images[0:4]
print(type(first))
print(first.shape)
#print(first)

predicted_classes = network.predict_classes(first)

print('')
print('predicted classification of the first four images:', predicted_classes)
print('')

network.save('kerasModel.model')


