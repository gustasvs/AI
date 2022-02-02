import gzip
import numpy as np
import random
import matplotlib.pyplot as plt
from functions.settings import *
from functions.functions import *


def main(): 
    garums = 0
    training_data = []

    image_size = 28
    num_images = 60000

    # imageset_training = gzip.open('data/t10k-images-idx3-ubyte.gz','r')
    # labelset_training = gzip.open('data/t10k-labels-idx1-ubyte.gz','r')
    imageset_training = gzip.open('data/train-images-idx3-ubyte.gz', 'r')
    labelset_training = gzip.open('data/train-labels-idx1-ubyte.gz','r')
    print("Loaded images")

    imageset_training.read(16)
    imageset_buffer = imageset_training.read(image_size * image_size * num_images)
    imageset_data = np.frombuffer(imageset_buffer, dtype=np.uint8).astype(np.float32)
    imageset_data = imageset_data.reshape(num_images, image_size, image_size, 1)

    labelset_training.read(8)
    labelset_buffer = labelset_training.read(num_images)
    labelset_data = np.frombuffer(labelset_buffer, dtype=np.uint8).astype(np.int64)

    image_array = []
    label_array = []

    for i in range(num_images):
        image_but_array = np.asarray(imageset_data[i]).squeeze()
        image_array.append(image_but_array)
        label_array.append(labelset_data[i])
    print("Preprocessed images")

    training_data = []
    garums = 0

    for _ in range(training_data_count):
        rnts = [random.randint(0, num_images - 2), random.randint(0, num_images - 2), random.randint(0, num_images - 2)]
        images = [image_array[rnts[0]], image_array[rnts[1]], image_array[rnts[2]]]
        skaitlis = str(label_array[rnts[0]]) + str(label_array[rnts[1]]) + str(label_array[rnts[2]])
        binary_skaitlis = number_to_binary_array(skaitlis)
        output_skaitlis = digit_to_array(skaitlis)
        
        training_image = unite_images(images, 5)

        #* print(binary_skaitlis)
        #* print(output_skaitlis)
        #* Image.fromarray((training_image).astype(np.uint8)).show()

        training_data.append([training_image, [output_skaitlis]])

        if len(training_data) % DATA_IN_ONE_FILE == 0:
            garums += len(training_data)
            training_data = np.array(training_data)
            print(garums)
            np.save("data/3digit/" + str(garums) + '.npy', training_data)
            training_data = []
    print(f"Finished creating data. Garums - > {garums}")

main()
