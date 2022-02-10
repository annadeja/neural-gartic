import tensorflow as tf
import numpy as np
import os

class DatasetProcessor(object):
    """Contains all the variables describing the locations of relevant data sets while also converting all the images into labeled data."""
    def __init__(self, path, width, height):
        super().__init__()

        self.train_path = os.path.join(path, 'train')
        self.valid_path = os.path.join(path, 'validate')
        self.width = width
        self.height = height
        self.classes = []
        self.train_paths = []
        self.valid_paths = []
        for class_name in os.scandir(self.train_path):
            if class_name.is_dir():
                class_name = class_name.name
                self.classes.append(class_name)
                self.train_paths.append(self.train_path + '\\' + class_name)
                self.valid_paths.append(self.valid_path + '\\' + class_name)

    def create_dataset(self, path):
        try:
            file_list_dataset = tf.data.Dataset.list_files(str(path + '\\*\\*'))
            labeled_dataset = file_list_dataset.map(self.label_image, num_parallel_calls = tf.data.experimental.AUTOTUNE)
            return labeled_dataset
        except UnicodeDecodeError:
            pass

    def make_batch(self, dataset, batch_size):
        try:
            dataset = dataset.cache()
            dataset = dataset.shuffle(buffer_size=1000)
            dataset = dataset.repeat()
            dataset = dataset.batch(batch_size)
            dataset = dataset.prefetch(buffer_size = tf.data.experimental.AUTOTUNE)

            return dataset
        except AttributeError:
            pass

    def label_image(self, file_path):
        image = tf.io.read_file(file_path)
        image = self.process_image(image)

        image_label = self.get_image_label(file_path)
        return image, image_label

    def process_image(self, image):
        image = tf.image.decode_jpeg(image, channels = 3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_flip_up_down(image)
        #image = tf.image.random_brightness(image, max_delta = 0.3)
        #image = tf.image.random_saturation(image, 0.0, 0.3)
        image = tf.image.rot90(image, tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.int32))
        return tf.image.resize(image, [self.width, self.height])
    
    def process_test_image(self, file_path):
        image = tf.io.read_file(file_path)
        image = tf.image.decode_jpeg(image, channels = 3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        return tf.image.resize(image, [self.width, self.height])

    #Getters:
    def get_image_label(self, file_path):
        pair = tf.strings.split(file_path, os.path.sep)
        return pair[-2] == self.classes

    def get_train_path(self):
        return self.train_path

    def get_valid_path(self):
        return self.valid_path

    def get_train_directory_size(self):
        size = 0
        try:
            for path in self.train_paths:
                size += len(os.listdir(path))
        except FileNotFoundError:
            pass
        return size

    def get_valid_directory_size(self):
        size = 0
        try:
            for path in self.valid_paths:
                size += len(os.listdir(path))
        except FileNotFoundError:
            pass
        return size

    #Setters:
    def set_path(self, path):
        self.train_path = os.path.join(path, 'train')
        self.valid_path = os.path.join(path, 'validate')
        self.train_paths.clear()
        self.valid_paths.clear()

        for class_name in self.classes:
            self.train_paths.append(self.train_path + '\\' + class_name)
            self.valid_paths.append(self.valid_path + '\\' + class_name)