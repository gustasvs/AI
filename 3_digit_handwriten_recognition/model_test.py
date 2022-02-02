import numpy as np
import cv2
import time
import os
import random
import colorama
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
import matplotlib.pyplot as plt
from functions.getkeys import key_check
from functions.settings import *
from functions.functions import *
from models import inception_v3 as googlenet
from models import alexnet

colorama.init()

#!fix gpu overflow
import tensorflow as tf    
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

#!fix numpy loading
np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

WIDTH = ekplat
HEIGHT = ekgar
MODEL_NAME = '{}-{}-epochs.model'.format('alexnet', EPOCHS * (training_data_count))

model = alexnet(WIDTH, HEIGHT, LR, output = output_lenght)
# model = googlenet(WIDTH, HEIGHT, 1, LR, output=output_lenght, model_name=MODEL_NAME)
model.load(f'model/{MODEL_NAME}')

def main():
    # test_data = np.load(f'data/artura_paraugi/10.npy')
    # for i in range(10):
    #     result_image = Image.fromarray((test_data[i][0]).astype(np.uint8))#.show()
    #     result_image = np.asarray(result_image).reshape(WIDTH,HEIGHT,1)
    #     prediction = model.predict([result_image])[0]
    #     f_array, s_array, t_array, first, second, third = prediction_to_number(prediction)
    #     print(digit_to_array_reversed(test_data[i][1][0]))
    #     print(first, second, third)
    #     Image.fromarray((test_data[i][0]).astype(np.uint8)).show()

    for i in range(0, 4):
        image = Image.open(f"data/artura_paraugi/{i}.jpg")
        image = image.resize((60, 30))

        pixel_values_newimg1_1dlist = list(image.getdata())

        pixel_values_image = []
        semi_list = []
        for obj in pixel_values_newimg1_1dlist:
            semi_list.append(obj)
            if len(semi_list) == WIDTH:
                pixel_values_image.append(semi_list)
                semi_list = []

        result_image = []
        pixel_value_bg = getBackgroundColor(pixel_values_image)

        for x in range(HEIGHT):
            list_array = []
            for y in range(WIDTH):
                r = pixel_values_image[x][y][0]
                g = pixel_values_image[x][y][1]
                b = pixel_values_image[x][y][2]
                pixel_value = round(0.2989 * r + 0.5870 * g + 0.1140 * b)

                if pixel_value > pixel_value_bg - 30 and pixel_value < pixel_value_bg + 30:
                    pixel_value = 0
                else:
                    pixel_value = 256 - pixel_value

                if (pixel_value > 60):
                    pixel_value = min(pixel_value * 1.3, 255)
                else:
                    pixel_value = max(0, pixel_value / 2.5)

                list_array.append(pixel_value)
            result_image.append(list_array)
        result_image = np.asarray(result_image).reshape(WIDTH,HEIGHT,1)
        # Image.fromarray((result_image).astype(np.uint8)).show()
        prediction = model.predict([result_image])[0]
        f_array, s_array, t_array, first, second, third = prediction_to_number(prediction)
        print(first, second, third)
        # print(prediction)
        # print(f"First digit:")
        # for i in range(0,10):
        #     print(round(prediction[i], 3), end=" ")
        # print(binary_array_to_number(prediction))

main()
