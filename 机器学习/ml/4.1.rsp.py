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


def get_files():
    rock_files = os.listdir(rock_dir)
    paper_files = os.listdir(paper_dir)
    scissors_files = os.listdir(scissors_dir)
    return rock_files, paper_files, scissors_files


def show(rock_files, paper_files, scissors_files):
    pic_index = 2
    next_rock = [os.path.join(rock_dir, fname)
                 for fname in rock_files[pic_index - 2:pic_index]]
    next_paper = [os.path.join(paper_dir, fname)
                  for fname in paper_files[pic_index - 2:pic_index]]
    next_scissors = [os.path.join(scissors_dir, fname)
                     for fname in scissors_files[pic_index - 2:pic_index]]

    for i, img_path in enumerate(next_rock + next_paper + next_scissors):
        # print(img_path)
        img = mpimg.imread(img_path)
        plt.imshow(img)
        plt.axis('Off')
        plt.show()


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
    validation_datagen = ImageDataGenerator(rescale = 1./255)

    train_generator = training_datagen.flow_from_directory(
        TRAINING_DIR,
        target_size=(150, 150),
        class_mode='categorical',
        batch_size=64
    )
    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=(150, 150),
        class_mode='categorical',
        batch_size=64
    )

    return train_generator, validation_generator


def get_model():
    model = tf.keras.models.Sequential([
        # Note the input shape is the desired size of the image 150x150 with 3 bytes color
        # This is the first convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The second convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The third convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The fourth convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # Flatten the results to feed into a DNN
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        # 512 neuron hidden layer
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    model.summary()
    return model


def training(model, train_generator, validation_generator):
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    history = model.fit(train_generator, epochs=25, steps_per_epoch=20, validation_data=validation_generator, verbose=1,
                        validation_steps=3)
    model.save(MODEL_FILE)  # save model
    return history, model


def analysis(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend(loc=0)
    plt.figure()

    plt.show()


def analysis2(model, test_datagen):
    filenames = test_datagen.filenames
    nb_samples = len(filenames)
    classifications = model.predict_generator(test_datagen, steps=nb_samples)
    print(classifications)
    preds = classifications.round(decimals=2)
    for p in preds:
        print(p)

    # show result
    test_file_names = test_datagen.filenames  # sequential list of name of test files of each sample
    test_labels =  test_datagen.labels  # is a sequential list  of test labels for each image sample
    class_dict =  test_datagen.class_indices  # a dictionary where key is the class name and value is the corresponding label for the class
    print(class_dict)  # have a look at the dictionary
    new_dict = {}
    for key in class_dict:  # set key in new_dict to value in class_dict and value in new_dict to key in class_dict
        value = class_dict[key]
        new_dict[value] = key
    print('PREDICTED CLASS  TRUE CLASS       FILENAME ')  # adjust spacing based on your class names
    total = 0
    correct = 0
    for i, p in enumerate(preds):
        pred_index = np.argmax(p)  # get the index that has the highest probability
        pred_class = new_dict[pred_index]  # find the predicted class based on the index
        true_class = new_dict[test_labels[i]]  # use the test label to get the true class of the test file
        file = test_file_names[i]
        print(f'    {pred_class}       {true_class}       {file}')
        if pred_class == true_class:
            correct += 1
        total += 1
    print("correct rate: ", correct/total)


def main():
    #rock_files, paper_files, scissors_files = get_files()
    #show(rock_files, paper_files, scissors_files)
    train_generator, test_generator = get_training_data()
    model = get_model()
    history, model = training(model, train_generator, test_generator)
    analysis(history)
    analysis2(model, test_generator)


main()
