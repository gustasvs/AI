import numpy as np
import cv2
import time
import os
import random
import colorama
from functions.grabscreen import grab_screen
from functions.getkeys import key_check
from functions.settings import *
from alexnet import alexnet
from models import inception_v3 as googlenet
from functions.directkeys import PressKey, ReleaseKey, W, A, S, D
from vjoy import vJoy, ultimate_release

colorama.init()
vj = vJoy()

WIDTH = ekplat // resize_dala
HEIGHT = ekgar // resize_dala
LR = 1e-3
EPOCHS = 8
BATCH_SIZE = 64
BALANCED_FILE_COUNT = 4

MODEL_NAME = '{}-{}-{}-epochs.model'.format(file_name, 'alexnet', EPOCHS * (balanced_file_count - 1))
model = alexnet(WIDTH, HEIGHT, LR, output = buttons)
# model = googlenet(WIDTH, HEIGHT, 1, LR, output=buttons, model_name=MODEL_NAME)
model.load(f'model/{MODEL_NAME}')

def countdown(laiks):
    for i in list(range(laiks))[::-1]:
        print(i + 1, end = '\r')
        time.sleep(1)

vj.open()
joystickPosition = vj.generateJoystickPosition()
vj.update(joystickPosition)
time.sleep(0.001)
vj.close()

# main script
def main():
    XYRANGE = 16393
    ZRANGE = 32786
    # countdown()
    last_time = time.time()  
    paused = False  

    while True:

        screen = grab_screen(region=(0, 40, ekplat, ekgar)) # ekrana izmeri
        screen = cv2.resize(screen, (ekplat // resize_dala, ekgar // resize_dala)) # Nomaina izmeru
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) # Uz melnbaltu

        last_time = time.time()

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
        if (turn > 0):
            turn = max(turn - w, 0)
        elif (turn < 0):
            turn = min(turn + w, 0)


        if not paused:

            vj.open()
            joystickPosition = vj.generateJoystickPosition(wAxisX = XYRANGE + int(round(XYRANGE * turn)))
            vj.update(joystickPosition)
            vj.close()

            # if (gas > 0):
            #     PressKey(W)
            #     ReleaseKey(S)
            # else: 
            #     PressKey(S)
            #     ReleaseKey(W)

        # print(gas, turn, prediction, end = '\r')
        if len(str(int(round(abs(gas * 100))))) < 3: 
            sgas = str(int(round(abs(gas * 100)))) + (3 - len(str(int(round(abs(gas * 100)))))) * " "
        else: sgas = str(int(round(abs(gas * 100))))
        sture = ['<' for i in range(10)]
        sture.append('|')
        for i in range(11): sture.append('>')
        sture[10 + int(round(turn * 10))] = colorama.Fore.LIGHTMAGENTA_EX + sture[10 + int(round(turn * 10))] + colorama.Fore.RESET
        ssture = ''
        for i in sture: ssture += str(i)
        print(colorama.Fore.GREEN if gas > 0 else colorama.Fore.RED, sgas, colorama.Fore.RESET, ssture, round(w + a + s + d + wa + wd + nk), end = '\r')

        # pause
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                vj.open()
                joystickPosition = vj.generateJoystickPosition(wAxisZRot = 0)
                vj.update(joystickPosition)
                time.sleep(1)
                vj.close()

main()
