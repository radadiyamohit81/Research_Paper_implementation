# -*- coding: utf-8 -*-
"""cifar-Alexnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17GCSR2J39ejtPzPWdWeiTV3NPMwJanF9

## Imports
"""

import keras
import os
import tensorflow as tf
from keras.callbacks import CSVLogger, EarlyStopping
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import  Conv2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD

"""## Dataset and preprocessing"""

# Define the parameters for the training
batch_size = 128
num_classes = 10 
epochs = 100 
num_predictions = 20
save_dir = os.path.join(os.getcwd(), 'saved_models') 
model_name = 'keras_cifar10_trained_model.h5' # Model name

# Splits the data between train and test sets
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# Converts the vectors to one hot encoding
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

"""## Model"""

model = Sequential()

#Layer 1 
model.add(Conv2D(filters=48, kernel_size=(3,3), 
                 strides=(1,1), padding='same', 
                 input_shape=(32,32,3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)) )

#Layer 2
model.add(Conv2D(filters=96, kernel_size=(3,3), padding='same') )
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

#Layer 3
model.add(Conv2D(filters=192, kernel_size=(3,3), 
                  activation='relu', padding='same') )

#Layer 4
model.add(Conv2D(filters=192, kernel_size=(3,3), 
                  activation='relu', padding='same') )

#Layer 5
model.add(Conv2D(filters=256, kernel_size=(3,3), 
                 activation='relu', padding='same') )
model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)) )

model.add(Flatten())

#Layer 6
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))

#Layer 7 
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

#Prediction
model.add(Dense(10))
model.add(BatchNormalization())
model.add(Activation('softmax'))

model.compile(loss="categorical_crossentropy",
              optimizer=SGD(lr=0.01, momentum=0.9, decay=0.0005),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          shuffle=True,
          epochs=100,
          validation_data=(x_test, y_test),
          callbacks=[EarlyStopping(min_delta=0.001, patience=3)])

# Evaluate the model
scores = model.evaluate(x_test, y_test)

print('Loss: %.3f' % scores[0])
print('Accuracy: %.3f' % scores[1])

# Commented out IPython magic to ensure Python compatibility.
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

Y_pred = model.predict(x_test, verbose=2)
y_pred = np.argmax(Y_pred, axis=1)
 
for ix in range(10):
    print(ix, confusion_matrix(np.argmax(y_test,axis=1),y_pred)[ix].sum())
cm = confusion_matrix(np.argmax(y_test,axis=1),y_pred)
print(cm)
 
# Visualizing of confusion matrix
import seaborn as sn
import pandas  as pd
 
 
df_cm = pd.DataFrame(cm, range(10),
                  range(10))
plt.figure(figsize = (10,7))
sn.set(font_scale=1.4)#for label size
sn.heatmap(df_cm, annot=True,annot_kws={"size": 12})# font size
plt.show()

