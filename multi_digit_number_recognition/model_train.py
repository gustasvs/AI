import numpy as np
import cv2
import time
import os
import pandas as pd
from tqdm import tqdm
from functions.settings import *
from collections import deque
from models import inception_v3 as googlenet
from models import alexnet
from random import shuffle

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
MODEL_NAME = '{}-{}-iterations.model'.format('alexnet', EPOCHS * (training_data_count))

# model = googlenet(WIDTH, HEIGHT, 1, LR, output=output_lenght, model_name=MODEL_NAME)
model = alexnet(WIDTH, HEIGHT, LR, output = output_lenght)

model.load(f'model/{MODEL_NAME}')

for epoch in range(16):

    data_order = [i for i in range(1, int(training_data_count * 10 / DATA_IN_ONE_FILE))]
    shuffle(data_order)

    for i in data_order:
        try:
            train_data = np.load(f'data/huge/{i * DATA_IN_ONE_FILE}.npy')

            train = train_data[:-50]
            test = train_data[-50:]

            inputs = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
            targets = [i[1][0] for i in train]
            # print (targets[0])
            # time.sleep(10)
            test_inputs = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
            test_targets = [i[1][0] for i in test]

            model.fit({'input': inputs}, {'targets': targets}, n_epoch=1, 
            validation_set=({'input': test_inputs}, {'targets': test_targets}), 
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME, batch_size=BATCH_SIZE)

            model.save(f'model/{MODEL_NAME}')
                    
        except Exception as e:
            print(str(e))
