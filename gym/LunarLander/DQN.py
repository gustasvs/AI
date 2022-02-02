from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import adam
import numpy

class ReplayBuffer(object):
    def __init__(self, max_size, input_shape, n_actions, discrete = False):
        self.mem_size = max_size
        self.discrete = discrete
        self.state_memory = numpy.zeros((self.mem_size, input_shape))
        self.new_state_memory = numpy.zeros((self.mem_size, input_shape))
        if self.discrete:
            dtype = numpy.int8
        else:
            dtype = numpy.float32
        self.action_memory = numpy.zeros((self.mem_size, n_actions), dtype=dtype)
        self.reward_memory = numpy.zeros(self.mem_size)
        self.terminal_memory = numpy.zeros(self.mem_size, dtype=numpy.float32)
        self.mem_cntr = 0

    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)
        if self.discrete:
            actions = numpy.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.mem_cntr += 1
    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = numpy.random.choice(max_mem, batch_size)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, new_states, terminal

def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    model = Sequential([
        Dense(fc1_dims, input_shape = (input_dims,)),
        Activation('relu'),
        Dense(fc2_dims),
        Activation('relu'),
        Dense(n_actions)
    ])
    model.compile(optimizer = adam(lr = lr), loss = 'mse')
    
    return model

class Agent(object):
    def __init__(self, alpha, gamma, n_actions, epsilon,
     batch_size, input_dims, epsilon_dec = 0.996, epsilon_end = 0.01,
     mem_size = 1000000, fname = 'dqn_modelis.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_name = fname

        self.memory = ReplayBuffer(mem_size, input_dims, n_actions, discrete=True)
        
        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)

    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        state = state[numpy.newaxis, :]
        rand = numpy.random.random()
        if rand < self.epsilon:
            action = numpy.random.choice(self.action_space)
        else:
            actions = self.q_eval.predict(state)
            action = numpy.argmax(actions)
        
        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return
        state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)
        action_values = numpy.array(self.action_space, dtype=numpy.int8)
        action_indices = numpy.dot(action, action_values)

        q_eval = self.q_eval.predict(state)
        q_next = self.q_eval.predict(new_state)
        q_target = q_eval.copy()

        batch_index = numpy.arange(self.batch_size, dtype=numpy.int32)

        q_target[batch_index, action_indices] = reward + \
             self.gamma*numpy.max(q_next, axis=1)*done

        _ = self.q_eval.fit(state, q_target, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min 

    def save_model(self):
        self.q_eval.save(self.model_name)

    def load_model(self):
        self.q_eval = load_model(self.model_name)