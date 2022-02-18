import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
from DatasetProcessor import DatasetProcessor
from bing_image_downloader import downloader

import os
import sys
import threading
import math
import numpy as np
import matplotlib.pyplot as plt


class NetworkContainer(object):
    """Contains all the data and fuctions relevant to working with the neural network."""

    def __init__(self, path):
        super().__init__()

        self.batch_size = 5
        self.epochs = 150
        self.height = 200
        self.width = 200

        self.path = path
        self.model = None
        self.dataset_processor = DatasetProcessor(self.path, self.width, self.height)
        self.is_running = False

    def train_network(self):
        self.is_running = True
        self.has_failed = False
        labeled_dataset = self.dataset_processor.create_dataset(self.dataset_processor.get_train_path())
        train_dataset = self.dataset_processor.make_batch(labeled_dataset, self.batch_size)
        labeled_dataset = self.dataset_processor.create_dataset(self.dataset_processor.get_valid_path())
        valid_dataset = self.dataset_processor.make_batch(labeled_dataset, self.batch_size)
        if train_dataset == None or valid_dataset == None:
            print('Looks like you selected an invalid directory. Select one containing subdirectories "train" and "validate" with proper classes instead.')
            self.is_running = False
            return
        
        if self.model == None:
            self.model = self.create_model()
            self.model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5), loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

        self.model.summary()

        history = self.model.fit(train_dataset, steps_per_epoch = math.ceil(self.dataset_processor.get_train_directory_size() / self.batch_size),
            epochs=self.epochs, validation_data=valid_dataset, validation_steps = math.ceil(self.dataset_processor.get_valid_directory_size() / self.batch_size))
        self.plot_data(history)

        self.is_running = False

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

    def predict_class(self, file_path):
        if self.model != None:
            image = self.dataset_processor.process_test_image(file_path)
            return self.model.predict(image[np.newaxis, ...], batch_size = 1)

    def create_model(self):
        return Sequential([
            Conv2D(16, (7, 7), padding='same', activation='relu', strides=(2, 2), input_shape=(self.height, self.width, 1), kernel_regularizer=regularizers.l2(0.001)),
            BatchNormalization(),
            #MaxPooling2D(),
            #Conv2D(128, 3, padding='same', activation='relu'),
            #MaxPooling2D(),
            #Conv2D(16, 3, padding='same', activation='relu'),
            #MaxPooling2D(),
            #Conv2D(128, 3, padding='same', activation='relu'),
            #MaxPooling2D(),
            Conv2D(32, (5,5), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            #BatchNormalization(),
            #MaxPooling2D(),
            #Conv2D(32, (3,3), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.0001)),
            Dropout(0.25),
            Conv2D(64, (5,5), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            #Conv2D(64, (3,3), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.0001)),
            #MaxPooling2D(),
            #BatchNormalization(),
            Dropout(0.25),
            Conv2D(128, (3,3), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            #Conv2D(128, (3,3), padding='same', activation='relu', strides=(2, 2), kernel_regularizer=regularizers.l2(0.001)),
            #MaxPooling2D(),
            Dropout(0.5),
            Flatten(),
            Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            #Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            #Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            #Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            #Dense(16, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.5),
            Dense(len(self.dataset_processor.classes), activation='softmax')
            ])

    def save_model(self, path):
        if self.model != None:
            self.model.save(path + '.h5')

    def load_model(self, path):
        if path != '':
            self.model = tf.keras.models.load_model(path)

    def is_model_empty(self):
        if self.model == None:
            return True
        else:
            return False

    #Setters:
    def set_path(self, path):
        self.dataset_processor.set_path(path)

    def set_epochs(self, epochs):
        self.epochs = epochs

    #Getters:
    def get_is_running(self):
        return self.is_running

    def get_epochs(self):
        return self.epochs

def main():
    #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    #downloader.download("watermelondrawing", limit=70,  output_dir='D:\\Program Files\\neural-gartic\\NeuralNet\\data\\train\\watermelon', adult_filter_off=True, force_replace=False, timeout=1000, verbose=True)
    network_container = NetworkContainer(os.getcwd() + "\\data")
    network_container.train_network()
    network_container.save_model("modelv1")

if __name__ == "__main__":
    main()