

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, utils
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import seaborn as sn
import numpy as np

labels_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
num_classes = 10

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plt.rcParams['figure.figsize'] = [20, 10]

# built-in mnist digit dataset.
data = keras.datasets.mnist
print(data)
print(type(data))

# we seperate the data into parts. 60000 train samples and 10000 test samples.
(x_train, y_train), (x_test, y_test) = data.load_data()
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

# we show part the data:
print(x_train[0])
print(f'The actual Label is: {y_train[0]}')
plt.imshow(x_train[0], cmap=plt.cm.binary) # the image isn't colored, but black-n-white.
plt.show()

# we show part the data:
print(x_test[0])
print(f'The actual Label is: {y_test[0]}')
plt.imshow(x_test[0])
plt.show()

# we show the distribution in labels belonging to training data.
(unique, counts) = np.unique(y_train, return_counts=True)
frequencies = np.asarray((unique, counts)).T
print(frequencies)

# we show the distribution in labels belonging to testing data.
(unique, counts) = np.unique(y_test, return_counts=True)
frequencies = np.asarray((unique, counts)).T
print(frequencies)

# we have to normalize the data, so the time taken for training would be low.
# first approach:
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

print(x_train[0])
plt.imshow(x_train[0], cmap=plt.cm.binary) # the image isn't colored, but black-n-white.
plt.show()

print(x_test[0])
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.show()

# we have to normalize the data, so the time taken for training would be low.
# second approach:
x_train = utils.normalize(x_train, axis=1)
x_test = utils.normalize(x_test, axis=1)

print(x_train[0])
plt.imshow(x_train[0], cmap=plt.cm.binary) # the image isn't colored, but black-n-white.
plt.show()

print(x_test[0])
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.show()

# we have to reshape our train/test data in order for our model to work.
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

print(x_train.shape)
print(x_test.shape)

# we have to categorize our labels so the model would work easily. not essential, but, better.
y_train = utils.to_categorical(y_train, 10)
y_test = utils.to_categorical(y_test, 10)

print(y_train.shape)
print(y_test.shape)

# after preporcessing, we create our model:
model = keras.Sequential()

# first complex (containing three layers):
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=(28, 28, 1), padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

# second complex (containing three layers):
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

# third complex (containing three layers):
model.add(Conv2D(filters=16, kernel_size=(5, 5), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

# tenth layer:
model.add(Flatten()) # since the output of convolution layers is multi-dimensional, we need this layer to flatten the results before going on in our network..

# eleventh layer:
model.add(Dense(128, activation='relu'))

# twelfth layer:
model.add(Dense(num_classes, activation='softmax'))

# we then compile our model, ready to be used.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# a summary of the architecture of our neural network.
model.summary()

history = model.fit(x_train, y_train, validation_split=0.15, batch_size=8, epochs=5)

utils.plot_model(model, show_shapes=True, dpi=120)

# we evaluate our model:
plt.subplot(2, 1, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.7, 1])
plt.legend(loc='best')
plt.show()

# we evaluate our model:
plt.subplot(2, 1, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='best')
plt.show()

# accuracy score:
_, accuracy = model.evaluate(x_test, y_test, verbose=2)
predictions = model.predict(x_test)
predictions = np.argmax(predictions, axis=1)
print(accuracy)

y_test = np.argmax(y_test, axis=1)

# precision score:
precision = precision_score(y_test, predictions, average='macro')
print(f'Precision: {precision}')

# recall score:
recall = recall_score(y_test, predictions, average='macro')
print(f'Recall: {recall}')

# f1-score score:
f1 = f1_score(y_test, predictions, average='macro')
print(f'f1-score: {f1}')

# confusion matrix:
cm = confusion_matrix(y_test, predictions, labels=labels_numbers)
df_cm = pd.DataFrame(cm, index=labels_numbers, columns=labels_numbers)
sn.heatmap(df_cm, annot=True)
plt.show()