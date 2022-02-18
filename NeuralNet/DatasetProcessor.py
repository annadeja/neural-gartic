import tensorflow as tf
import numpy as np
import os

##Contains all the variables describing the locations of relevant data sets while also converting all the images into labeled data.
class DatasetProcessor(object):
    ##The constructor.
    #@param self The current object.
    #@param path Location of the dataset.
    #@param width The width to which images will be scaled.
    #@param height The height to which images will be scaled.
    def __init__(self, path, width, height):
        super().__init__()
        ##The location of the training dataset.
        self.train_path = os.path.join(path, 'train')
        ##The location of the validation dataset.
        self.valid_path = os.path.join(path, 'validate')
        ##The width to which images will be scaled.
        self.width = width
        ##The height to which images will be scaled.
        self.height = height
        ##Stores the classes of data.
        self.classes = []
        ##Stores the locations of folders pertaining to all training classes.
        self.train_paths = []
        ##Stores the locations of folders pertaining to all validation classes.
        self.valid_paths = []
        for class_name in os.scandir(self.train_path):
            if class_name.is_dir():
                class_name = class_name.name
                self.classes.append(class_name)
                self.train_paths.append(self.train_path + '\\' + class_name)
                self.valid_paths.append(self.valid_path + '\\' + class_name)

    ##Function responsible for creating the labeled dataset.
    #@param self The current object.
    #@param path Location of the dataset.
    def create_dataset(self, path):
        try:
            file_list_dataset = tf.data.Dataset.list_files(str(path + '\\*\\*'))
            labeled_dataset = file_list_dataset.map(self.label_image, num_parallel_calls = tf.data.experimental.AUTOTUNE)
            return labeled_dataset
        except UnicodeDecodeError:
            pass

    ##Function responsible for cutting a dataset into batches of a specific size.
    #@param self The current object.
    #@param dataset Object containing the loaded dataset.
    #@param batch_size Specifies the size of a single batch.
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

    ##Function responsible for mapping a class label to a single image.
    #@param self The current object.
    #@param file_path Location of an image.
    def label_image(self, file_path):
        image = tf.io.read_file(file_path)
        image = self.process_image(image)

        image_label = self.get_image_label(file_path)
        return image, image_label

    ##Function responsible for decoding, resizing and augmenting an image.
    #@param self The current object.
    #@param image Object containing a loaded image.
    def process_image(self, image):
        image = tf.image.decode_jpeg(image, channels = 1)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_flip_up_down(image)
        image = tf.image.rot90(image, tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.int32))
        return tf.image.resize(image, [self.width, self.height])

    #Getters:

    ##Function responsible for returning a class label in form of a boolean variable.
    #@param self The current object.
    #@param file_path Location of an image.
    def get_image_label(self, file_path):
        pair = tf.strings.split(file_path, os.path.sep)
        return pair[-2] == self.classes

    ##Function responsible for returning the location of the training dataset.
    #@param self The current object.
    def get_train_path(self):
        return self.train_path

    ##Function responsible for returning the location of the validation dataset.
    #@param self The current object.
    def get_valid_path(self):
        return self.valid_path

    ##Function responsible for returning the size of the training dataset.
    #@param self The current object.
    def get_train_directory_size(self):
        size = 0
        try:
            for path in self.train_paths:
                size += len(os.listdir(path))
        except FileNotFoundError:
            pass
        return size

    ##Function responsible for returning the size of the validation dataset.
    #@param self The current object.
    def get_valid_directory_size(self):
        size = 0
        try:
            for path in self.valid_paths:
                size += len(os.listdir(path))
        except FileNotFoundError:
            pass
        return size