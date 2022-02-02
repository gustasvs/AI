import numpy as np

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

from functions.settings import *

end = list()

for e in range(1000, 31000, 1000):
    print(e)
    end = end + list(np.load("data/" + file_name + "_" + str(e) + ".npy"))


np.save("data/" + file_name + '.npy', end)
