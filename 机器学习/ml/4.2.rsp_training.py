import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np

TRAINING_DIR = 'rock-paper-scissors/rps'
VALIDATION_DIR = 'rock-paper-scissors/rps-test-set'

MODEL_FILE = 'rps_model.h5'

rock_dir = os.path.join(TRAINING_DIR + '/rock')
paper_dir = os.path.join(TRAINING_DIR + '/paper')
scissors_dir = os.path.join(TRAINING_DIR + '/scissors')


def get_training_data():
    training_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    train_generator = training_datagen.flow_from_directory(
        TRAINING_DIR,
        target_size=(150, 150),
        class_mode='categorical',
        batch_size=64
    )

    return train_generator


def get_model():
    model = tf.keras.models.Sequential([
        # Note the input shape is the desired size of the image 150x150 with 3 bytes color
        # This is the first convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The second convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The third convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The fourth convolution
        #tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        #tf.keras.layers.MaxPooling2D(2, 2),
        # Flatten the results to feed into a DNN
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        # 512 neuron hidden layer
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    model.summary()
    return model


def training(model, train_generator):
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.fit(train_generator, epochs=15, steps_per_epoch=20, verbose=1)
    return model


def main():
    train_generator = get_training_data()
    model = get_model()
    model = training(model, train_generator)

    model.save(MODEL_FILE)  # save model

main()
