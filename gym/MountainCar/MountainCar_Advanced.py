import gym
import numpy as np
import matplotlib.pyplot as plt # grafosanai

env = gym.make("MountainCar-v0")

LEARNING_RATE = 0.1 # no 0 lidz 1
DISCOUNT = 0.95 # cik svariga ir nakotne pret tagadni (no 0 lidz 1)
EPISODES = 25000
EPSILON = 0.5 #cik daudz random (exploratory)
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
EPSILON_DECAY_VALUE = EPSILON/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)
SHOW_EVERY = 2000

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high) # 2 vai cik daudz lietas redz lmao
DISCRETE_OS_WIN_SIZE = (env.observation_space.high-env.observation_space.low) / DISCRETE_OS_SIZE

q_table = np.random.uniform(low = -2, high = 0, size = (DISCRETE_OS_SIZE + [env.action_space.n])) # all combinations  * all actions :)))
#q_table = np.load('79000-qtable.npy')

ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / DISCRETE_OS_WIN_SIZE
    return tuple(discrete_state.astype(np.int))

for episode in range(EPISODES):
    episode_reward = 0
    if episode % SHOW_EVERY == 0:
        render = True
        print(episode)
    else:
        render = False
    discrete_state = get_discrete_state(env.reset())
    done = False
    while not done:
        if np.random.random() > EPSILON:    
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, env.action_space.n)
        new_state, reward, done, _ = env.step(action)
        episode_reward += reward
        new_discrete_state = get_discrete_state(new_state)
        if render:
            env.render() # show
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action, )]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q) # formula
            q_table[discrete_state + (action, )] = new_q
        # Simulation ended (for any reson) - if goal position is achived - update Q value with reward directly
        elif new_state[0] >= 0.5:
            #q_table[discrete_state + (action,)] = reward
            print(f"Finisheja {episode} episodee LMAO!")
            q_table[discrete_state + (action,)] = 0
        discrete_state = new_discrete_state
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        EPSILON -= EPSILON_DECAY_VALUE
    ep_rewards.append(episode_reward)
    if not episode % 1000:
        np.save(f"q_tables/{episode}-qtable", q_table)

    if not episode % SHOW_EVERY:
        #np.save(f"q_tables/{episode}-qtable", q_table)
        average_reward = sum(ep_rewards[-SHOW_EVERY:]) / len(ep_rewards[-SHOW_EVERY:])
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))
        print(f"Episode: {episode} avg: {average_reward} min: {min(ep_rewards[-SHOW_EVERY:])} max: {max(ep_rewards[-SHOW_EVERY:])}")
env.close()
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label = "avg")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label = "min")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label = "max")
plt.legend(loc = 2)
plt.show()