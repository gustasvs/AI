from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add


class DQNAgent(object):

    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        # self.learning_rate = 0.0005
        self.learning_rate = 0.001
        #self.model = self.network()
        self.model = self.network("weights.hdf5")
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game, chuska, food):
        state = [
            (chuska.x_change == 20 and chuska.y_change == 0 and ((list(map(add, chuska.position[-1], [20, 0])) in chuska.position) or
            chuska.position[-1][0] + 20 >= (game.ekplat - 20))) or (chuska.x_change == -20 and chuska.y_change == 0 and ((list(map(add, chuska.position[-1], [-20, 0])) in chuska.position) or
            chuska.position[-1][0] - 20 < 20)) or (chuska.x_change == 0 and chuska.y_change == -20 and ((list(map(add, chuska.position[-1], [0, -20])) in chuska.position) or
            chuska.position[-1][-1] - 20 < 20)) or (chuska.x_change == 0 and chuska.y_change == 20 and ((list(map(add, chuska.position[-1], [0, 20])) in chuska.position) or
            chuska.position[-1][-1] + 20 >= (game.ekgar-20))),  # danger straight

            (chuska.x_change == 0 and chuska.y_change == -20 and ((list(map(add,chuska.position[-1],[20, 0])) in chuska.position) or
            chuska.position[ -1][0] + 20 > (game.ekplat-20))) or (chuska.x_change == 0 and chuska.y_change == 20 and ((list(map(add,chuska.position[-1],
            [-20,0])) in chuska.position) or chuska.position[-1][0] - 20 < 20)) or (chuska.x_change == -20 and chuska.y_change == 0 and ((list(map(
            add,chuska.position[-1],[0,-20])) in chuska.position) or chuska.position[-1][-1] - 20 < 20)) or (chuska.x_change == 20 and chuska.y_change == 0 and (
            (list(map(add,chuska.position[-1],[0,20])) in chuska.position) or chuska.position[-1][
             -1] + 20 >= (game.ekgar-20))),  # danger right

             (chuska.x_change == 0 and chuska.y_change == 20 and ((list(map(add,chuska.position[-1],[20,0])) in chuska.position) or
             chuska.position[-1][0] + 20 > (game.ekplat-20))) or (chuska.x_change == 0 and chuska.y_change == -20 and ((list(map(
             add, chuska.position[-1],[-20,0])) in chuska.position) or chuska.position[-1][0] - 20 < 20)) or (chuska.x_change == 20 and chuska.y_change == 0 and (
            (list(map(add,chuska.position[-1],[0,-20])) in chuska.position) or chuska.position[-1][-1] - 20 < 20)) or (
            chuska.x_change == -20 and chuska.y_change == 0 and ((list(map(add,chuska.position[-1],[0,20])) in chuska.position) or
            chuska.position[-1][-1] + 20 >= (game.ekgar-20))), #danger left


            chuska.x_change == -20,  # move left
            chuska.x_change == 20,  # move right
            chuska.y_change == -20,  # move up
            chuska.y_change == 20,  # move down
            food.x_food < chuska.x,  # food left
            food.x_food > chuska.x,  # food right
            food.y_food < chuska.y,  # food up
            food.y_food > chuska.y  # food down
            ]

        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0

        return np.asarray(state)

    def set_reward(self, chuska, crash):
        self.reward = 0
        if crash:
            self.reward = -10
            return self.reward
        if chuska.paedis:
            self.reward = 10
        return self.reward

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=11))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)
