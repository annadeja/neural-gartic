import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
from DatasetProcessor import DatasetProcessor

import os
import sys
import threading
import math
import numpy as np
import matplotlib.pyplot as plt

##Contains all the data and fuctions relevant to working with the neural network.
class NetworkContainer(object):
    ##The constructor.
    #@param self The current object.
    #@param path Location of the dataset.
    def __init__(self, path):
        super().__init__()
        ##Specifies the size of a single batch.
        self.batch_size = 5
        ##Specifies the number of epochs that the network will run for.
        self.epochs = 150
        ##The height to which images will be scaled.
        self.height = 200
        ##The width to which images will be scaled.
        self.width = 200
        ##The location of the dataset.
        self.path = path
        ##Holds the neural network model.
        self.model = None
        ##Holds the object responsible for processing training data.
        self.dataset_processor = DatasetProcessor(self.path, self.width, self.height)

    ##Function responsible for preparing data and training the neural network.
    #@param self The current object.
    def train_network(self):
        labeled_dataset = self.dataset_processor.create_dataset(self.dataset_processor.get_train_path())
        train_dataset = self.dataset_processor.make_batch(labeled_dataset, self.batch_size)
        labeled_dataset = self.dataset_processor.create_dataset(self.dataset_processor.get_valid_path())
        valid_dataset = self.dataset_processor.make_batch(labeled_dataset, self.batch_size)
        if train_dataset == None or valid_dataset == None:
            print('Looks like you selected an invalid directory. Select one containing subdirectories "train" and "validate" with proper classes instead.')
            return
        
        if self.model == None:
            self.model = self.create_model()
            self.model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5), loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

        self.model.summary()

        history = self.model.fit(train_dataset, steps_per_epoch = math.ceil(self.dataset_processor.get_train_directory_size() / self.batch_size),
            epochs=self.epochs, validation_data=valid_dataset, validation_steps = math.ceil(self.dataset_processor.get_valid_directory_size() / self.batch_size))
        self.plot_data(history)

    ##Function responsible for plotting the data collected during training.
    #@param self The current object.
    #@param history Data collected during the training process.
    def plot_data(self, history):
        epochs_range = range(self.epochs)
        accuracy = history.history['accuracy']
        valid_accuracy = history.history['val_accuracy']

        loss = history.history['loss']
        valid_loss = history.history['val_loss']

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, accuracy, label='Training Accuracy')
        plt.plot(epochs_range, valid_accuracy, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, valid_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

    ##Function responsible for creating the neural network model.
    #@param self The current object.
    def create_model(self):
        return Sequential([
            Conv2D(16, (7, 7), padding='same', activation='relu', strides=(2, 2), input_shape=(self.height, self.width, 1), kernel_regularizer=regularizers.l2(0.001)),
            BatchNormalization(),
            Conv2D(32, (5,5), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.25),
            Conv2D(64, (5,5), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.25),
            Conv2D(128, (3,3), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.5),
            Flatten(),
            Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.5),
            Dense(len(self.dataset_processor.classes), activation='softmax')
            ])
    
    ##Function responsible for saving the trained neural network model to a file.
    #@param self The current object.
    #@param path The location to which the model will be saved.
    def save_model(self, path):
        if self.model != None:
            self.model.save(path + '.h5')

##Function responsible for setting off the training process.
def main():
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    network_container = NetworkContainer(os.getcwd() + "\\data")
    network_container.train_network()
    network_container.save_model("modelv1")

if __name__ == "__main__":
    main()