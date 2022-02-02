import numpy as np
from functions.grabscreen import grab_screen
import cv2
import time
import os
import pandas as pd
from tqdm import tqdm
from alexnet import alexnet
from functions.settings import *
from collections import deque
from models import inception_v3 as googlenet
from random import shuffle

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

WIDTH = ekplat // resize_dala
HEIGHT = ekgar // resize_dala
LR = 1e-3
EPOCHS = 32
BATCH_SIZE = 64
BALANCED_FILE_COUNT = 4
MODEL_NAME = '{}-{}-{}-epochs.model'.format(file_name, 'alexnet', EPOCHS * (BALANCED_FILE_COUNT - 1))

# model = googlenet(WIDTH, HEIGHT, 1, LR, output=buttons, model_name=MODEL_NAME)
model = alexnet(WIDTH, HEIGHT, LR, output = buttons)

model.load(f'model/{MODEL_NAME}')

for epoch in range(EPOCHS):

    data_order = [i for i in range(1, BALANCED_FILE_COUNT)]
    shuffle(data_order)

    for i in data_order:
        try:
            train_data = np.load(f'data/{file_name}_balanced_{i}.npy')

            train = train_data[:-50]
            test = train_data[-50:]

            inputs = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
            targets = [i[1] for i in train]
            test_inputs = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
            test_targets = [i[1] for i in test]

            model.fit({'input': inputs}, {'targets': targets}, n_epoch=1, 
            validation_set=({'input': test_inputs}, {'targets': test_targets}), 
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME, batch_size=BATCH_SIZE)

            model.save(f'model/{MODEL_NAME}')
                    
        except Exception as e:
            print(str(e))
