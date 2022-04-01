import numpy as np
import matplotlib.pyplot as plt

# Function that calculates moving average of a series
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# Function that plots scores and epsilon against number of episodes
def plot_scores_epsilon(rewards_history, epsilon_history, moving_avg_window=100):
    
    team_rewards = [sum(x) for x in zip(*rewards_history)]
    
    f, axarr = plt.subplots(1,2, figsize=(10,3))
    for i in range(len(rewards_history)):
        axarr[0].plot(movingaverage(np.array(rewards_history[i]), moving_avg_window), label=f'Agent {i+1} (MA)')
    axarr[0].plot(movingaverage(np.array(team_rewards), moving_avg_window), label=f'Team rewards (MA)')
    axarr[0].set_xlabel('Episodes')
    axarr[0].set_ylabel('Scores')
    axarr[0].legend()

    axarr[1].plot(epsilon_history, label='epsilon')
    axarr[1].set_xlabel('Episodes')
    axarr[1].set_ylabel('Epsilon')
    axarr[1].legend()

    plt.show()