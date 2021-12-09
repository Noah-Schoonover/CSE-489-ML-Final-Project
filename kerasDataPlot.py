import numpy as np
from keras.datasets import mnist
import ConsolePlot as cp
from matplotlib import pyplot as plt

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = np.where(train_images > 70, 255, 0)
test_images = np.where(test_images > 70, 255, 0)

print('')
print('shape of training images Tensor:',train_images.shape)
print('shape of test images Tensor:',test_images.shape)
print('')

overlayed = np.mean(train_images, axis=0)

plt.imshow(overlayed)
plt.show()
