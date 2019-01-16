# Neural network based on https://nextjournal.com/gkoehler/digit-recognition-with-keras

# imports for arrays and plotting
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# keras imports for datasets and neural network
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils

# loading dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# plot some data
fig = plt.figure()
for i in range(100,109,1):
    plt.subplot(3,3,i-99)
    plt.tight_layout()
    plt.imshow(X_train[i], cmap='gray', interpolation='none')
    plt.title('Digit:'+str(y_train[i]))
    plt.xticks([])
    plt.yticks([])
    
# plot pixel distribution
fig2 = plt.figure()
plt.subplot(2,1,1)
plt.imshow(X_train[0], cmap='gray', interpolation='none')
plt.title('Digit:'+str(y_train[0]))
plt.xticks([])
plt.yticks([])
plt.subplot(2,1,2)
plt.hist(X_train[0].reshape(784))
plt.title('Pixel Value Distribution')

# =============================================================================
# # print shape before reshaping
# print("X_train shape", X_train.shape)
# print("y_train shape", y_train.shape)
# print("X_test shape", X_test.shape)
# print("y_test shape", y_test.shape)
# =============================================================================

# reshaping 28x28 matric to vector
# bulding the input vector from the 28x28 pixels
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

# normalizing the data
X_train /= 255
X_test /= 255

# =============================================================================
# # =============================================================================
# # # print ready input shape
# # print('Train matrix shape: '+str(X_train.shape))
# # print('Test matrix shape: '+str(X_test.shape))
# # =============================================================================
# 
# # creating dummy variables from y
# # one-hot encoding 
# # print("Shape before one-hot encoding: ", y_train.shape)
# Y_train = np_utils.to_categorical(y_train, 10)
# Y_test = np_utils.to_categorical(y_test, 10)
# # print("Shape after one-hot encoding: ", Y_train.shape)
# 
# 
# # bulding a neural network's layers
# # first hidden layer
# model = Sequential()
# model.add(Dense(512, input_shape=(784,)))
# model.add(Activation('relu'))
# model.add(Dropout(0.2))
# 
# # second hidden layer
# model.add(Dense(512))
# model.add(Activation('relu'))
# model.add(Dropout(0.2))
# 
# # output Layer
# model.add(Dense(10))
# model.add(Activation('softmax'))
# 
# # compiling the model
# model.compile(loss='categorical_crossentropy', metrics=['accuracy'], 
#               optimizer='adam')
# 
# 
# # fit the model
# readyModel = model.fit(X_train, Y_train, batch_size=128, epochs=20, verbose=2,
#                        validation_data=(X_test, Y_test))
# 
# # saving the model
# model.save('digitRecognizer.h5')
# print('Saved trained model as digitRecognizer.h5')
# 
# # plotting the metrics
# fig3 = plt.figure()
# plt.subplot(2,1,1)
# plt.plot(readyModel.history['acc'])
# plt.plot(readyModel.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='lower right')
# 
# plt.subplot(2,1,2)
# plt.plot(readyModel.history['loss'])
# plt.plot(readyModel.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper right')
# 
# plt.tight_layout()
# =============================================================================

mnist_model = load_model('digitRecognizer.h5')

predicted_classes = mnist_model.predict_classes(X_test)

# see which we predicted correctly and which not
correct_indices = np.nonzero(predicted_classes == y_test)[0]
incorrect_indices = np.nonzero(predicted_classes != y_test)[0]
print()
print(len(correct_indices)," classified correctly")
print(len(incorrect_indices)," classified incorrectly")

