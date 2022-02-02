import pygame
from random import randint, choice
from QLearning import DQNAgent
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

ziimet = False
speed = 10
pygame.font.init()
cikDaudz = 5000
kadzim = 0
class Game:
    def __init__(self, ekplat , ekgar):
        pygame.display.set_caption('Qlirning')
        self.ekplat = ekplat
        self.ekgar = ekgar
        self.gameDisplay = pygame.display.set_mode((ekplat, ekgar+60))
        self.bg = pygame.image.load("img/background.png")
        self.crash = False
        self.chuska = chuska(self)
        self.food = Food()
        self.score = 0

class chuska(object):
    def __init__(self, game):
        x = 0.45 * game.ekplat
        y = 0.5 * game.ekgar
        self.x = x - x % 20
        self.y = y - y % 20
        self.position = []
        self.position.append([self.x, self.y])
        self.food = 1
        self.paedis = False
        self.image = pygame.image.load('img/snakeBody.png')
        self.x_change = 20
        self.y_change = 0

    def update_position(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 0:
                for i in range(0, self.food - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, move, x, y, game, food,agent):
        move_array = [self.x_change, self.y_change]

        if self.paedis:

            self.position.append([self.x, self.y])
            self.paedis = False
            self.food = self.food + 1
        if np.array_equal(move ,[1, 0, 0]):
            move_array = self.x_change, self.y_change
        elif np.array_equal(move,[0, 1, 0]) and self.y_change == 0:
            move_array = [0, self.x_change]
        elif np.array_equal(move,[0, 1, 0]) and self.x_change == 0: 
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:
            move_array = [0, -self.x_change]
        elif np.array_equal(move,[0, 0, 1]) and self.x_change == 0:
            move_array = [self.y_change, 0]
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        if self.x < 20 or self.x > game.ekplat-40 or self.y < 20 or self.y > game.ekgar-40 or [self.x, self.y] in self.position:
            game.crash = True
        est(self, food, game)

        self.update_position(self.x, self.y)

    def display_chuska(self, x, y, food, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if game.crash == False:
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))

            pygame.display.update()
        else:
            pygame.time.wait(300)

class Food(object):
    def __init__(self):
        self.x_food = 240
        self.y_food = 200
        self.image = pygame.image.load('img/food2.png')
    def food_coord(self, game, chuska):
        x_rand = randint(20, game.ekplat - 40) #choice([40, game.ekplat - 60]) 
        self.x_food = x_rand - x_rand % 20
        y_rand = randint(20, game.ekgar - 40) #choice([40, game.ekgar - 60]) 
        self.y_food = y_rand - y_rand % 20
        if [self.x_food, self.y_food] not in chuska.position:
            return self.x_food, self.y_food
        else:
            self.food_coord(game,chuska)
    def display_food(self, x, y, game):
        game.gameDisplay.blit(self.image, (x, y))
        pygame.display.update()


def est(chuska, food, game):
    if chuska.x == food.x_food and chuska.y == food.y_food:
        food.food_coord(game, chuska)
        chuska.paedis = True
        game.score = game.score + 1
def get_record(score, record):
        if score >= record:
            return score
        else:
            return record
def display_ui(game, score, record):
    myfont = pygame.font.SysFont('Segoe UI', 20)
    myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
    text_score = myfont_bold.render('rez: ', True, (0, 0, 0))
    text_score_number = myfont_bold.render(str(score), True, (0, 0, 0))
    text_highest = myfont_bold.render('labak rez: ', True, (0, 0, 0))
    text_highest_number = myfont_bold.render(str(record), True, (0, 0, 0))
    game.gameDisplay.blit(text_score, (70, 440))
    game.gameDisplay.blit(text_score_number, (110, 440))
    game.gameDisplay.blit(text_highest, (200, 440))
    game.gameDisplay.blit(text_highest_number, (300, 440))
    game.gameDisplay.blit(game.bg, (10, 10))
def display(chuska, food, game, record):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score, record)
    chuska.display_chuska(chuska.position[-1][0], chuska.position[-1][1], chuska.food, game)
    food.display_food(food.x_food, food.y_food, game)
def initialize_game(chuska, game, food, agent):
    state_init1 = agent.get_state(game, chuska, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    chuska.do_move(action, chuska.x, chuska.y, game, food, agent)
    state_init2 = agent.get_state(game, chuska, food)
    reward1 = agent.set_reward(chuska, game.crash)
    agent.remember(state_init1, action, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory)
def grafs(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color':'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()
def run():
    pygame.init()
    agent = DQNAgent()
    skaits = 0
    score_plot = []
    counter_plot =[]
    record = 0
    ziimet = False
    while skaits < cikDaudz:
        if kadzim < skaits:
            ziimet = True
        # Initialize classes
        game = Game(440, 440)
        chuska1 = game.chuska
        food1 = game.food

        # Perform first move
        initialize_game(chuska1, game, food1, agent)
        if ziimet:
            display(chuska1, food1, game, record)

        while not game.crash:
            agent.epsilon = 80 - skaits
            state_old = agent.get_state(game, chuska1, food1)
            if randint(0, 200) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                prediction = agent.model.predict(state_old.reshape((1,11)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)
            chuska1.do_move(final_move, chuska1.x, chuska1.y, game, food1, agent)
            state_new = agent.get_state(game, chuska1, food1)
            reward = agent.set_reward(chuska1, game.crash)
            agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
            agent.remember(state_old, final_move, reward, state_new, game.crash)
            record = get_record(game.score, record)
            if kadzim < skaits:
                ziimet = True
            if ziimet:
                display(chuska1, food1, game, record)
                pygame.time.wait(speed)

        agent.replay_new(agent.memory)
        skaits += 1
        print('Iter', skaits, '   Rez:', game.score)
        score_plot.append(game.score)
        counter_plot.append(skaits)
    agent.model.save_weights('weights.hdf5')
    grafs(counter_plot, score_plot)
run()
