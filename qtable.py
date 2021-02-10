import numpy as np

from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, ITEMS_PER_STACK
from actions import Actions
from util import nPr

class QTable:
    def __init__(self):
        num_states = (nPr(N_ROWS*N_COLS, N_ROBOTS) 
                      * nPr(N_ROWS*N_COLS, N_STACKS)
                      * 2**N_ROBOTS 
                      * (ITEMS_PER_STACK+1)**N_STACKS)
        
        num_actions = len(Actions().valid_actions)**N_ROBOTS
        self.qvals = np.zeros((num_states, num_actions))
        self.visits = np.zeros((num_states, num_actions))
        self.learning_rate = 0.8
        self.discount_factor = 0.8
        return
    
    def update(self, s1, s2, a, r):
        s1num = s1.enum()
        s2num = s2.enum()
        anum = a.enum()
        
        old_val = self.qvals[s1num][anum]
        min_val = min(self.qvals[s2num][np.logical_not(np.isnan(self.qvals[s2num]))])
        self.qvals[s1num][anum] += self.learning_rate*(r + self.discount_factor*(min_val) - old_val)
        self.visits[s1num][anum] += 1
        return
    
    def __repr__(self):
        return str(self.qvals) + '\n\n' + str(self.visits)
    