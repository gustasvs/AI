import numpy as np
import os
import time
import cv2
from tqdm import tqdm
from alexnet import alexnet
from settings import *
from models import inception_v3 as googlenet
from random import shuffle

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

WIDTH = ekplat // resize_dala
HEIGHT = ekgar // resize_dala
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'pyDiRT-{}-{}-epochs.model'.format('alexnet', EPOCHS)

# model = googlenet(WIDTH, HEIGHT, 1, LR, output=buttons, model_name=MODEL_NAME)
model = alexnet(WIDTH, HEIGHT, LR, output = buttons)

train_data = np.load(file_name + '_balanced.npy')

train = train_data[:-50]
test = train_data[-50:]

X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, 
validation_set=({'input': test_x}, {'targets': test_y}), 
snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)

# tensorboard --logdir=foo:C:/Python123/AI/gtatoDiRT/log