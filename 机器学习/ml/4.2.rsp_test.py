from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import numpy as np

VALIDATION_DIR = 'rock-paper-scissors/rps-test-set'
MODEL_FILE = 'rps_model.h5'


def get_test_data():
    validation_datagen = ImageDataGenerator(rescale = 1./255)
    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=(150, 150),
        class_mode='categorical',
        batch_size=64
    )
    return validation_generator


def get_model():
    return load_model(MODEL_FILE)


def analysis(model):
    test_datagen = get_test_data()
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
    model = get_model()
    get_test_data()
    analysis(model)


main()
