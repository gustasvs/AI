import gzip
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from functions.settings import *
from functions.functions import *


def main(): 

    garums = 0

    training_data = []

    for _ in range(training_data_count):
    # for _ in range(1000000):
        skaitlis = random3digitNumberGenerator()
        image_data = create_image(skaitlis)
        image_distorted = distortImage(image_data, random.randint(8, 10))
 
        image_array = np.asarray(image_distorted)
        output_skaitlis = digit_to_array(skaitlis)
        
        print(skaitlis)
        plt.imshow(image_array, interpolation='nearest'); plt.show()
        
        training_data.append([image_array, [output_skaitlis]])

        if len(training_data) % DATA_IN_ONE_FILE == 0:
            garums += len(training_data)
            training_data = np.array(training_data)
            print(garums)
            # np.save("data/3digit/" + str(garums) + '.npy', training_data)
            np.save("data/huge/" + str(garums) + '.npy', training_data)
            training_data = []
    print(f"Finished creating data. Garums - > {garums}")

main()
