import os
import zipfile
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image


def load_data():
    local_zip = 'data/horse-or-human.zip'
    zip_ref = zipfile.ZipFile(local_zip, 'r')
    r = zip_ref.extractall('horse-or-human')
    zip_ref.close()

    # Directory with our training horse and human pictures
    train_horse_dir = os.path.join('horse-or-human/horses')
    train_human_dir = os.path.join('horse-or-human/humans')

    train_horse_names = os.listdir(train_horse_dir)
    print(train_horse_names[:10])
    train_human_names = os.listdir(train_human_dir)
    print(train_human_names[:10])

    print('total training horse images:', len(os.listdir(train_horse_dir)))
    print('total training human images:', len(os.listdir(train_human_dir)))
    return train_horse_dir, train_human_dir, train_horse_names, train_human_names


def show_images(train_horse_dir, train_human_dir, train_horse_names, train_human_names):
    # Parameters for our graph; we'll output images in a 4x4 configuration
    nrows = 4
    ncols = 4

    # Index for iterating over images
    pic_index = 0

    fig = plt.gcf()
    fig.set_size_inches(ncols * 4, nrows * 4)

    pic_index += 8
    next_horse_pix = [os.path.join(train_horse_dir, fname)
                      for fname in train_horse_names[pic_index - 8:pic_index]]
    next_human_pix = [os.path.join(train_human_dir, fname)
                      for fname in train_human_names[pic_index - 8:pic_index]]

    for i, img_path in enumerate(next_horse_pix + next_human_pix):
        # Set up subplot; subplot indices start at 1
        sp = plt.subplot(nrows, ncols, i + 1)
        sp.axis('Off')  # Don't show axes (or gridlines)

        img = mpimg.imread(img_path)
        plt.imshow(img)

    plt.show()


def get_model():
    model = tf.keras.models.Sequential([
        # Note the input shape is the desired size of the image 300x300 with 3 bytes color
        # This is the first convolution
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(300, 300, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The second convolution
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The third convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The fourth convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The fifth convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # Flatten the results to feed into a DNN
        tf.keras.layers.Flatten(),
        # 512 neuron hidden layer
        tf.keras.layers.Dense(512, activation='relu'),
        # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('horses') and 1 for the other ('humans')
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.summary()
    return model


def predict(model, folder, type):
    test_dir = os.path.join(folder)
    test_names = os.listdir(test_dir)
    print(test_names[:10])

    correct = 0
    total = 0
    for fn in test_names:
        path = folder + fn
        #path = "horse-or-human/humans/" + fn
        img = image.load_img(path, target_size=(300, 300))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)

        if classes[0] > 0.5:
            print(fn + " is a human", classes[0])
            if type == 'human':
                correct += 1
        else:
            print(fn + " is a horse", classes[0])
            if type == 'horse':
                correct += 1

        total += 1
    return correct, total


def main():
    train_horse_dir, train_human_dir, train_horse_names, train_human_names = load_data()
    show_images(train_horse_dir, train_human_dir, train_horse_names, train_human_names)
    model = get_model()
    model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(learning_rate=0.001),
              metrics=['acc'])

    train_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(
        'horse-or-human/',  # This is the source directory for training images
        target_size=(300, 300),  # All images will be resized to 150x150
        batch_size=128,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

    history = model.fit(
        train_generator,
        steps_per_epoch=8,
        epochs=20,
        verbose=1)

    correct1, total1 = predict(model, 'test_data/humans/', 'human')

    correct2, total2 = predict(model, 'test_data/horses/', 'horse')
    print("human rate: correct = ", correct1, ", total = ", total1, ", rate = ", correct1 / total1)
    print("horse rate: correct = ", correct2, ", total = ", total2, ", rate = ", correct2/total2)


main()