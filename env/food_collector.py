import numpy as np
import gym
from gym import spaces
import matplotlib.pyplot as plt
import sys

# import env_control
from env_control import Env_control
from multi_agent_spaces import MultiAgentActionSpace, MultiAgentObservationSpace

class Food_Collector_Env(gym.Env):
    def __init__(self, grid_size=[11,11], n_agents=2):
        self.n_agents = n_agents
        self.grid_size = grid_size.copy()
        self.viewer = None
        
        self.action_space = MultiAgentActionSpace([spaces.Discrete(4) for _ in range(self.n_agents)])
        self.observation_space = MultiAgentObservationSpace([spaces.Box(-8, 8, shape=(7,)) for _ in range(self.n_agents)])
    
    def step(self, action):
        self.last_state, reward, done, info = self.env_control.step(action)
        return self.last_state, reward, done, info
    
    def render(self, mode='human', close=False, frame_speed=.1):
        if self.viewer is None:
            self.fig = plt.figure(figsize=(5,5))
            self.viewer = self.fig.add_subplot(111)
            plt.ion()
            self.fig.show()
        else:
            self.viewer.clear()
            # Change color of one agent
            temp_grid = self.env_control.grid.grid.copy()
            temp_agent_pos = self.env_control.agents[0].pos.copy()
            temp_grid[temp_agent_pos[0], temp_agent_pos[1], :] = np.array([255,120,0], dtype=np.uint8)
        
            self.viewer.imshow(temp_grid)
            plt.pause(frame_speed)
        self.fig.canvas.draw()
    
    def reset(self):
        self.env_control = Env_control(self.grid_size.copy(), n_agents=self.n_agents)
        self.last_state = self.env_control.reset()
        return self.last_state
    
    def seed(self, seed):
        pass