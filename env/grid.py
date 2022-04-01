import numpy as np

class Grid():
    
    AGENT_COLOR = np.array([255,0,0], dtype=np.uint8)
    SPACE_COLOR = np.array([0,0,0], dtype=np.uint8) # background color
    FOOD_COLOR  = np.array([1,255,0], dtype=np.uint8)
    WALL_COLOR  = np.array([100,100,100], dtype=np.uint8)
    HOME_COLOR  = np.array([3,0,255], dtype=np.uint8)
    #OBJECT_COLOR = np.array([3,0,0], dtype=np.uint8)
    
    
    def __init__(self, grid_size=[20,20]):
        
        # get dimensions of grid
        self.grid_size = np.asarray(grid_size, dtype=np.int)
        self.height = self.grid_size[0].copy()
        self.width = self.grid_size[1].copy()
        
        # Create grid and fill with background color
        self.grid = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.grid[:,:,:]  = self.SPACE_COLOR
        
        # Create walls on the edges
        self.grid[:,0,:]  = self.WALL_COLOR
        self.grid[:,-1,:] = self.WALL_COLOR
        self.grid[0,:,:]  = self.WALL_COLOR
        self.grid[-1,:,:] = self.WALL_COLOR
        
        # Create home
        home_x_middle = self.width//2
        self.home_coors = [self.height-3, self.height-1, home_x_middle-1, home_x_middle+2] # For drawing
        self.home_goal_coor = [self.height-2, home_x_middle]  # For defining goal (x,y)
        self.grid[self.home_coors[0]:self.home_coors[1], self.home_coors[2]:self.home_coors[3], :] = self.HOME_COLOR
        
        # variable for storing food position
        self.food = list()
        
        # for reset
        self.save_grid = self.grid.copy()
        
    
    def reset(self):
        self.grid = self.save_grid.copy()
        self.place_food_random()
    
    def get_color(self, coor):
        # coor is as (x,y) but color is (r,g,b)
        return self.grid[coor[0], coor[1], :]
    
    def check_food_eaten(self, coor):
        # coor needs to be where agent WANTS to go 
        # i.e. agent moved so coors of agent location are updated, but grid not yet
        square_color = self.get_color(coor)
        return np.array_equal(square_color, self.FOOD_COLOR)
    
    def check_home_reached(self, coor):
        square_color = self.get_color(coor)
        return np.array_equal(square_color, self.HOME_COLOR)
        
    def place_food_random(self, num_foods=1):
        for _ in range(num_foods):
            while True:
                new_x = np.random.randint(1, self.height-2)
                new_y = np.random.randint(1, self.width-1)
                
                if np.array_equal(self.grid[new_x, new_y, :], self.SPACE_COLOR):
                    # place food
                    self.grid[new_x, new_y, :] = self.FOOD_COLOR
                    self.food = [new_x, new_y]
                    break
    
    def erase_cell(self, coor):
        self.grid[coor[0], coor[1], :] = self.SPACE_COLOR
        
    def draw_agent(self, coor):
        self.grid[coor[0], coor[1], :] = self.AGENT_COLOR
        
    def draw_home(self):
        self.grid[self.home_coors[0]:self.home_coors[1], self.home_coors[2]:self.home_coors[3], :] = self.HOME_COLOR
        
    def check_legal_space(self, coor):
        square_color = self.get_color(coor)
        return not np.array_equal(square_color, self.WALL_COLOR)
    
    # Unused in the final version
    # def get_state(self):
    #     return self.grid.copy()
    
    def get_state_discrete(self, agent_pos_list):
        '''
        agent_pos_list -> [[x1,y1], [x2,y2], ...]
        '''
        
        #initialise state
        # end goal is [[all state vars for agent1], [all state vars for agent2], ...]
        state = [ [] for _ in agent_pos_list]
        
        # DISTANCE TO FOOD
        for i in range(len(agent_pos_list)):
            agent_pos = agent_pos_list[i]
            x_dist_to_food = agent_pos[0] - self.food[0]
            y_dist_to_food = agent_pos[1] - self.food[1]
            state[i].extend([x_dist_to_food, y_dist_to_food])
        
        # DISTANCE TO HOME
        for i in range(len(agent_pos_list)):
            agent_pos = agent_pos_list[i]
            x_dist_to_home = agent_pos[0] - self.home_goal_coor[0]
            y_dist_to_home = agent_pos[1] - self.home_goal_coor[1]
            state[i].extend([x_dist_to_home, y_dist_to_home])
            
        # DISTANCE TO OTHER AGENTS
        # go through all agent combinations
        for i in range(len(agent_pos_list)):
            agent_pos = agent_pos_list[i]   # current agent
            
            for j in range(len(agent_pos_list)): 
                if i==j: continue
                
                agent_2_pos = agent_pos_list[j]   # all other agents
                x_dist = agent_pos[0] - agent_2_pos[0]
                y_dist = agent_pos[1] - agent_2_pos[1]
                
                state[i].extend([x_dist, y_dist])
                    
        return state
    