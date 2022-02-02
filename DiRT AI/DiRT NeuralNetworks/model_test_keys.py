import numpy as np
import cv2
import time
import os
from functions.grabscreen import grab_screen
from functions.getkeys import key_check
from functions.settings import *
from alexnet import alexnet
from models import inception_v3 as googlenet
from functions.directkeys import PressKey, ReleaseKey, W, A, S, D

WIDTH = ekplat // resize_dala
HEIGHT = ekgar // resize_dala
LR = 1e-3
EPOCHS = 8

MODEL_NAME = '{}-{}-{}-epochs.model'.format(file_name, 'alexnet', EPOCHS)
model = alexnet(WIDTH, HEIGHT, LR, output = buttons)
# model = googlenet(WIDTH, HEIGHT, 1, LR, output=buttons, model_name=MODEL_NAME)
model.load(f'model/{MODEL_NAME}')


def countdown(laiks):
    for i in list(range(laiks))[::-1]:
        print(i + 1, end = '\r')
        time.sleep(1)

def main():
    os.system('cls')
    countdown(3)
    last_time = time.time()  
    paused = False  
    while True:
        screen = grab_screen(region=(0, 40, ekplat, ekgar)) # ekrana izmeri
        screen = cv2.resize(screen, (ekplat // resize_dala, ekgar // resize_dala)) # Nomaina izmeru
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) # Uz melnbaltu

        #print('FPS =  {}'.format(1 // (time.time()-last_time)))
        last_time = time.time()
        # Predicto labako gajienu padodot ekranu
        prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
        for e in range(buttons):
            prediction[e] = round(prediction[e], 2)
        
        # w a s d wa wd nk
        w  = prediction[0]
        a  = prediction[1]
        s  = prediction[2]
        d  = prediction[3]
        wa = prediction[4]
        wd = prediction[5] 
        nk = prediction[6]

        gas = w + wa + wd - nk - s
        turn = d + wd - a - wa

        gas = round(gas, 2)
        turn = round(turn, 2)

        turn_treshold = 0.2

        if not paused:
            if (abs(turn) < turn_treshold):
                ReleaseKey(A)
                ReleaseKey(D)
            if (turn < -turn_treshold):
                PressKey(A)
                ReleaseKey(D)
            if (turn > turn_treshold):
                PressKey(D)
                ReleaseKey(A)
            
            if (gas > 0):
                PressKey(W)
                ReleaseKey(S)
            if (gas < 0):
                PressKey(S)
                ReleaseKey(W)

        # print(prediction, f'\nturn -> {round(turn, 2)}\ngaze  -> {round(gas, 2)}', end='\r')
        print(gas, turn, prediction, end = '\r')

            
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(W)
                ReleaseKey(A)
                ReleaseKey(S)
                ReleaseKey(D)
                time.sleep(1)

main()