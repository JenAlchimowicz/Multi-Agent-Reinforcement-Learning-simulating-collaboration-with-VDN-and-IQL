import numpy as np

class Collector():
    def __init__(self, init_coor = [1,1]):
        self.pos = init_coor.copy() #position
        self.save_start_pos = init_coor.copy()
    
    def move(self, action):
        #clockwise: [up,right,down,left]
        # 0=up, 1=right, 2=down, 3=left, 4=stay
        
        # up
        if action == 0:
            self.pos[0] -= 1
        # right
        elif action == 1:
            self.pos[1] += 1
        #down
        elif action == 2:
            self.pos[0] += 1
        #left
        elif action == 3:
            self.pos[1] -= 1
        #stay
        elif action == 4:
            pass
            
    def provisional_move(self, action):
        #clockwise: [up,right,down,left]
        # 0=up, 1=right, 2=down, 3=left, 4=stay
        provisional_pos = self.pos.copy()
        # up
        if action == 0:
            provisional_pos[0] -= 1
        # right
        elif action == 1:
            provisional_pos[1] += 1
        #down
        elif action == 2:
            provisional_pos[0] += 1
        #left
        elif action == 3:
            provisional_pos[1] -= 1
        #stay
        elif action == 4:
            pass
        return provisional_pos
            
    def reset(self):
        self.pos = self.save_start_pos.copy()