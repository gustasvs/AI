from DQN import Agent
import numpy
import gym

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    n_games = 2000
    agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.005, input_dims=8, n_actions=4, mem_size=1000000, batch_size=64, epsilon_end=0.01)
    
    scores = []
    eps_history = []

    for e in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            if e > 10:
                env.render()
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = numpy.mean(scores[max(0, e-100):(e+1)])
        print('episodes ', e, 'score %.2f' % score, 'average score %2f' % avg_score)
    if e % 10 == 0 and e > 0:
        agent.save_model()