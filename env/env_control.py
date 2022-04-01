import numpy as np
from grid import Grid
from collector import Collector

# main env class
class Env_control():
    
    def __init__(self, grid_size=[11,11], n_agents=2):
        self.n_agents = n_agents
        
        # Initialise grid
        self.grid = Grid(grid_size)
        
        # Create a static list for initial position of agents
        self.init_coors_agents = [[9,3], [9,7], [9,5], [9,1], [9,9]]
        if self.n_agents > len(self.init_coors_agents):
            raise ValueError('n_agents too large, max agents = 5')
        
        # Create agents
        self.agents = []
        for i in range(self.n_agents):
            self.agents.append(Collector(init_coor=self.init_coors_agents[i]))

        self.done = False
        self.state = None
        self.food_eaten = 0  #0=not eaten, 1=eaten
    
    def step(self, action):

        rewards = [-0.1 for _ in range(self.n_agents)]
        info = [{} for _ in range(self.n_agents)]
        
        # Erase old positions
        for agent in self.agents:
            self.grid.erase_cell(agent.pos)
        
        # Move agents if actions are legal (don't move, just provisional move in case they bump into each other)
        provisional_positions = [ [] for _ in range(self.n_agents)]
        for i in range(self.n_agents):
            if self.check_legal_move(self.agents[i].pos, action[i]):
                provisional_positions[i].extend(self.agents[i].provisional_move(action[i]))
            else:
                provisional_positions[i].extend(self.agents[i].pos)
        
        
        # ENVIRONMENT DYNAMICS
        
        # Check if agents bump into each other
        if len(set([tuple(x) for x in provisional_positions])) < len(provisional_positions):
            rewards = [x-5 for x in rewards]
            # agents stay in old pos
        else:
            #move agents
            for i in range(self.n_agents):
                if self.check_legal_move(self.agents[i].pos, action[i]):
                    self.agents[i].move(action[i])
                else:
                    rewards[i] -= 1
        
        # Check if food eaten
        for i in range(self.n_agents):
            if self.grid.check_food_eaten(self.agents[i].pos):
                self.food_eaten=True
                rewards[i] += 10
                
                # check if other agent is nearby:
                for j in range(self.n_agents):
                    if i==j: continue
                    if self.check_near_agents(self.agents[i].pos, self.agents[j].pos):
                        rewards[i] += 5
                        rewards[j] += 5
        
        
        # Check if home reached
        reached_home = 0
        for agent in self.agents:
            if self.grid.check_home_reached(agent.pos) and self.food_eaten:
                reached_home+=1
        if reached_home == self.n_agents:
            rewards = [x+20 for x in rewards]
            self.done = True
        
        # Draw new agent
        self.grid.draw_home()
        for agent in self.agents:
            self.grid.draw_agent(agent.pos)
        
        
        self.state = self.get_state()
        done = [self.done for _ in range(self.n_agents)]
        
        return self.state, rewards, done, info
    
    
    def get_state(self):
        state = self.grid.get_state_discrete([agent.pos for agent in self.agents])
        for s in state:
            s.append(self.food_eaten)
        state = [tuple(s) for s in state]
        return state
    
    def reset(self):
        self.done = False
        self.grid.reset()
        for agent in self.agents:
            agent.reset()
            self.grid.draw_agent(agent.pos)
        return self.get_state()
    
    
    def check_legal_move(self, agent_coor, action):
        # if not .copy() it will change the original value
        coor = agent_coor.copy()
        # fake move
        if   action == 0: coor[0] -= 1 #up
        elif action == 1: coor[1] += 1 #right
        elif action == 2: coor[0] += 1 #down
        elif action == 3: coor[1] -= 1 #left
        elif action == 4: pass         #stay
        
        return self.grid.check_legal_space(coor)
        
    def check_near_agents(self, agent1_pos, agent2_pos):
        if np.abs(agent1_pos[0] - agent2_pos[0]) <= 1:
            if np.abs(agent1_pos[1] - agent2_pos[1]) <= 1:
                return True
        else: return False
        