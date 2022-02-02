import numpy as np
import cv2
import time
import os
from functions.grabscreen import grab_screen
from functions.getkeys import key_check
from functions.settings import *

if os.path.isfile(file_name + '.npy'):
    print('yes file :)')
    training_data = np.load(file_name + '.npy', allow_pickle=True)
    training_data = list(training_data)
else:
    print('no file :(')
    training_data = []

def keys_to_output(keys):
    #[W, A, S, D, WA, WD, NK]
    w  = [1,0,0,0,0,0,0]
    a  = [0,1,0,0,0,0,0]
    s  = [0,0,1,0,0,0,0]
    d  = [0,0,0,1,0,0,0]
    wa = [0,0,0,0,1,0,0]
    wd = [0,0,0,0,0,1,0]
    nk = [0,0,0,0,0,0,1]
    output = [0,0,0,0,0,0,0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk

    return output


def countdown():
    for i in list(range(3))[::-1]:
        print(i + 1)
        time.sleep(1)


def main():
    garums = 0
    training_data = []
    couter = 0
    paused = False  
   
    countdown()
    
    last_time = time.time() 
    
    while True:
        if not paused:
            screen = grab_screen(region=(0, 40, ekplat, ekgar)) # ekrana izmeri
            screen = cv2.resize(screen, (ekplat // resize_dala, ekgar // resize_dala)) # Nomaina izmeru
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) # Uz melnbaltu

            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])
            garums += 1

            # print(f'FPS = {1 // (time.time()-last_time)}')
            # last_time = time.time()
            if len(training_data) % 100 == 0:
                print(garums)
            if len(training_data) % 1000 == 0:
                np.save("data/" + file_name + "_" + str(garums) + '.npy', training_data)
                training_data = []
            
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('Not pausd!')
                countdown()
            else:
                paused = True
                print('pausd!!')
                countdown()

main()
