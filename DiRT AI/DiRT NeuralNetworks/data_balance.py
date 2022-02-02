import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from functions.settings import *
import cv2

train_data = np.load("data/" + file_name + '.npy', allow_pickle=True)

train_data_start = train_data

df = pd.DataFrame(train_data)
# print(df.head())
print(Counter(df[1].apply(str)))

print(f'total data    --> {len(train_data)}')
AA = []
DD = []
WW = []
WA = []
WD = []
SS = []
NK = []
nothing = []

shuffle(train_data)

for data in train_data:
    image = data[0]
    choice = data[1]
    if choice == [1, 0, 0, 0, 0, 0, 0]:
        WW.append([image, choice])
    elif choice == [0, 1, 0, 0, 0, 0, 0]:
        AA.append([image, choice])
    elif choice == [0, 0, 1, 0, 0, 0, 0]:
        SS.append([image, choice])
    elif choice == [0, 0, 0, 1, 0, 0, 0]:
        DD.append([image, choice])
    elif choice == [0, 0, 0, 0, 1, 0, 0]:
        WA.append([image, choice])
    elif choice == [0, 0, 0, 0, 0, 1, 0]:
        WD.append([image, choice])
    elif choice == [0, 0, 0, 0, 0, 0, 1]:
        NK.append([image, choice])

WA = WA[:len(WD)]
WD = WD[:len(WA)] 
WW = WW[:len(WD) * 2]
AA = AA[:len(DD)]
DD = DD[:len(AA)]
SS = SS[:len(DD)]
NK = NK[:len(DD)]

final_data = WW + AA + SS + DD + WA + WD + NK

shuffle(final_data)

print(f'balanced data --> {len(final_data)}')

print (f'w = {len(WW)}, a = {len(AA)}, s = {len(SS)}, d = {len(DD)}, wa = {len(WA)}, wd = {len(WD)}, nk = {len(NK)}')

final_part = []

j = 0
ii = 0
for i, data in enumerate(final_data, 1):
    ii = i
    final_part.append(data)
    if i % 5000 == 0:
        j += 1
        np.save("data/" + file_name + '_balanced_' + str(j) + '.npy', final_part)
        print(f'balanced lines - {i}, filename - {j}')
        final_part = []

np.save("data/" + file_name + '_balanced_' + str(j + 1) + '.npy', final_part)
print(f'balanced lines - {len(final_part) + ii}, filename - {j + 1}')

for data in train_data_start:
    image = data[0]
    choice = data[1]
    cv2.imshow('testt', image)
    # print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
