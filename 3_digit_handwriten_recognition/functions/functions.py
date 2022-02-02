from numpy.core.records import array
from functions.settings import *
import random
from PIL import Image
import numpy as np

def number_to_binary_array(n): #creates output array consisting of binary numbers from input number "n"
    n = int(n)
    output_string = bin(n).replace("0b", "")
    output_array = []
    for char in output_string:
        output_array.append(char)
    while len(output_array) < 10: # output array length should be 10 because that is binary unber lenght from 1-1000
        output_array.insert(0, "0")
    return output_array

def getBackgroundColor(pixel_values_image): # no 0 lidz 255
    r = pixel_values_image[1][1][0]
    g = pixel_values_image[1][1][1]
    b = pixel_values_image[1][1][2]
    pixel_value_bg = round(0.2989 * r + 0.5870 * g + 0.1140 * b)
    return pixel_value_bg

def prediction_to_number(n):
    first_digit = []
    max_first_digit = -1
    max_first_label = -1
    max_second_digit = -1
    max_second_label = -1
    max_third_digit = -1
    max_third_label = -1
    for i in range (0, int(output_lenght / 3)):
        digit = round(n[i], 3)
        if (digit > max_first_digit):
            max_first_digit = digit
            max_first_label = i
        first_digit.append(digit)
    second_digit = []
    for i in range (int(output_lenght / 3), int((output_lenght / 3) * 2)):
        digit = round(n[i], 3)
        if (digit > max_second_digit):
            max_second_digit = digit
            max_second_label = i
        second_digit.append(digit)
    third_digit = []
    for i in range (int((output_lenght / 3) * 2), output_lenght):
        digit = round(n[i], 3)
        if (digit > max_third_digit):
            max_third_digit = digit
            max_third_label = i
        third_digit.append(digit)
    max_second_label = str(max_second_label)[1]
    max_third_label = str(max_third_label)[1]
    return first_digit, second_digit, third_digit, max_first_label, max_second_label, max_third_label

def normalizeColor(intensity):
    iI      = intensity
    minI    = 86
    maxI    = 230
    minO    = 0
    maxO    = 255
    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO

def binary_array_to_number(binary_array): #creates output array consisting of binary numbers from input number "n"
    binary_string = ""
    for bnum in binary_array:
        bnum = str(round(int(bnum)))
        binary_string += bnum
    return int(binary_string, 2)

def digit_to_array(n):
    # array = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    array = [0] * output_lenght
    while(len(n) < 3):
        n = 0 + n
    array[int(n[0]) +  0] = "1"
    array[int(n[1]) + 10] = "1"
    array[int(n[2]) + 20] = "1"
    return array

def digit_to_array_reversed(n):
    first = 0
    second = 0
    third = 0
    for i in range (0, int(output_lenght / 3)):
        if n[i] == "1":
            first = i
    for i in range (int(output_lenght / 3), int((output_lenght / 3) * 2)):
        if n[i] == "1":
            second = i
    for i in range (int((output_lenght / 3) * 2), output_lenght):
        if n[i] == "1":
            third = i
    second = str(second)[1]
    third = str(third)[1]
    return str(first) + second + third
        
def unite_images(image_array, shift_range): #returns array of united image data
    shiftx = random.randint(-2, 2)
    shifty = random.randint(-2, 2)
    shift1y = random.randint(-shift_range,shift_range)
    shift2y = random.randint(-shift_range,shift_range)
    shift3y = random.randint(-shift_range,shift_range)

    img1 = Image.fromarray(image_array[0])
    img2 = Image.fromarray(image_array[1])
    img3 = Image.fromarray(image_array[2])

    nw = ekplat
    nh = ekgar

    newimg1 = Image.new('RGBA', size=(nw, nh), color=(0, 0, 0, 0))
    newimg1.paste(img1, (shiftx + (15 * 0), shifty + shift1y))

    newimg2 = Image.new('RGBA', size=(nw, nh), color=(0, 0, 0, 0))
    newimg2.paste(img2, (shiftx + (15 * 1), shifty + shift2y))

    newimg3 = Image.new('RGBA', size=(nw, nh), color=(0, 0, 0, 0))
    newimg3.paste(img3, (shiftx + (15 * 2), shifty + shift3y))
    
    pixel_values_newimg1_1dlist = list(newimg1.getdata())
    pixel_values_newimg2_1dlist = list(newimg2.getdata())
    pixel_values_newimg3_1dlist = list(newimg3.getdata())
    pixel_values_img1 = []
    pixel_values_img2 = []
    pixel_values_img3 = []
    semi_list = []
    for obj in pixel_values_newimg1_1dlist:
        semi_list.append(obj)
        if len(semi_list) == nw:
            pixel_values_img1.append(semi_list)
            semi_list = []
    semi_list = []
    for obj in pixel_values_newimg2_1dlist:
        semi_list.append(obj)
        if len(semi_list) == nw:
            pixel_values_img2.append(semi_list)
            semi_list = []
    for obj in pixel_values_newimg3_1dlist:
        semi_list.append(obj)
        if len(semi_list) == nw:
            pixel_values_img3.append(semi_list)
            semi_list = []
    result_array = []
    for x in range(nh):
        list_array = []
        for y in range(nw):
            r = max(pixel_values_img1[x][y][0], pixel_values_img2[x][y][0], pixel_values_img3[x][y][0])
            g = max(pixel_values_img1[x][y][1], pixel_values_img2[x][y][1], pixel_values_img3[x][y][1])
            b = max(pixel_values_img1[x][y][2], pixel_values_img2[x][y][2], pixel_values_img3[x][y][2])
            pixel_value = round(0.2989 * r + 0.5870 * g + 0.1140 * b)
            list_array.append(pixel_value)
        result_array.append(list_array)
    result_array = np.asarray(result_array)
    #* plt.imshow(result_array, interpolation='nearest')
    #* plt.show()
    return result_array