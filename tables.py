import numpy as np
import pandas as pd

from actions import Actions
from util import nCr
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, N_ITEMS, LEARNING_RATE, DISCOUNT_FACTOR

class Tables:
    """
    The tables used for training.
    
    The qvals table is mandatory for training but the visits and same_locs 
    tables are not. The visits table allows us to see which values are not 
    being visited and helps us identify problems in our code. The same_locs 
    table speeds up training by updating the q-values of all actions that do 
    not change the robot/stack locations each time an action does not change 
    the robot/stack locations.
    
    Attributes
    ----------
    qvals : NumPy Array
        An array containing estimates of the q-value for each state and 
        action. The array has 1 row for each state and 1 column for each 
        action.
    visits : NumPy Array
        An array containing the number of times each action has been taken in
        each state. The array has 1 row for each state and 1 column for each 
        action.
    same_locs : NumPy Array
        An array that indicates which actions do not change the locations of
        the robots/stacks for each state. A 1 indicates the location stays the 
        same after taking an action in a state. A 0 indicates the location 
        changes after taking an action in a state or that the action has not
        been tried in that state yet. The array has 1 row for each state and 1 
        column for each action.
    performance : Pandas DataFrame
        A dataframe indicating the performance of the greedy policy after 
        training for some number of iterations.
    """
    
    def __init__(self):
        """
        Initializes the tables.
        
        The q-values are initialized to a value of 10 since 10 seemed like an
        average q-value after the first 100000 iterations of training.
        
        The visits are initialized to zero since no actions have been taken 
        yet.

        The same_locs table is initalized to all 0s except for the first 
        column which is all 1s. The first column corresponds to the actions 
        ['O', 'O', ..., 'O'] which will never change the locations of 
        robots/stacks.
        
        Many times these tables are overwritten by csvs that have been saved
        after many iterations of training.
    
        Returns
        -------
        None.

        """
        num_states = (nCr(N_ROWS*N_COLS+1, N_ROBOTS) 
                      * nCr(N_ROWS*N_COLS+1, N_STACKS)    
                      * (N_ITEMS+1)**N_STACKS)
        num_actions = len(Actions().valid_actions)**N_ROBOTS
        
        self.qvals = np.ones((num_states, num_actions)) * (N_ROWS + N_COLS - 1) * N_STACKS
        self.visits = np.zeros((num_states, num_actions))
        self.same_locs = np.concatenate((np.ones((1, num_states)), 
                                         np.zeros((num_actions-1, num_states)))).transpose()
        self.performance = pd.DataFrame([], columns=['iters', 'score'])
        return
    
    def update(self, s1, s2, a, c):
        """
        Update the values in the Q-table after a time step.

        Parameters
        ----------
        s1 : State
            The previous state.
        s2 : State
            The resulting state after taking an action.
        a : Actions
            The actions taken.
        c : int
            The cost recieved at that time step.

        Returns
        -------
        None.

        """
        # check if locations are the same
        same_locs = True
        for i in range(N_ROBOTS):
            if s1.robot_locs[i] != s2.robot_locs[i]:
                same_locs = False
                break
        if same_locs:
            for j in range(N_STACKS):
                if s1.stack_locs[i] != s2.stack_locs[i]:
                    same_locs = False
                    break
        
        s1num = s1.enum()
        s2num = s2.enum()
        
        if not same_locs:
            anum = a.enum()
            self.same_locs[s1num][anum] = 0
            old_val = self.qvals[s1num][anum]
            min_val = min(self.qvals[s2num])
            self.qvals[s1num][anum] += LEARNING_RATE*(c + DISCOUNT_FACTOR*(min_val) - old_val)
            self.visits[s1num][anum] += 1
        else:
            # vectorize updates using numpy arrays
            self.same_locs[s1num][a.enum()] = 1
            anums = np.argwhere(self.same_locs[s1num] == 1).flatten()
            old_vals = self.qvals[s1num][anums]
            min_val = min(self.qvals[s2num])
            self.qvals[s1num][anums] += LEARNING_RATE*(c + DISCOUNT_FACTOR*(min_val) - old_vals)
            self.visits[s1num][anums] += 1

        return
    
    def read_tables(self):
        """
        Overwrite the tables with csvs that contain more accurate q-value 
        estimates.
        
        Read the csvs into Pandas DataFrames and convert these to NumPy Arrays.

        Returns
        -------
        None.

        """
        name = (str(N_ROWS) + 'x' + str(N_COLS) + 'grid_' 
                + str(N_ROBOTS) + 'robots_' + str(N_STACKS) + 'stacks_'
                + str(N_ITEMS) + 'items')
        
        qvals = pd.read_csv('Q-Tables/qtable_' + name + '.csv')
        visits = pd.read_csv('Visits/visits_' + name + '.csv')
        same_locs = pd.read_csv('SameLocs/samelocs_' + name + '.csv')
        self.performance = pd.read_csv('Performance/performance_' + name + '.csv')
        
        self.qvals = np.asarray(qvals)
        self.visits = np.asarray(visits)
        self.same_locs = np.asarray(same_locs)
        return
    
    def save_tables(self):
        """
        Save the tables to use again later on.
        
        Convert the NumPy Arrays to Pandas DataFrames and save these as csvs.

        Returns
        -------
        None.

        """
        name = (str(N_ROWS) + 'x' + str(N_COLS) + 'grid_' 
                + str(N_ROBOTS) + 'robots_' + str(N_STACKS) + 'stacks_'
                + str(N_ITEMS) + 'items')
        
        qvals = pd.DataFrame(self.qvals)
        visits = pd.DataFrame(self.visits)
        same_locs = pd.DataFrame(self.same_locs)
        
        qvals.to_csv('Q-Tables/qtable_' + name + '.csv', index=False)
        visits.to_csv('Visits/visits_' + name + '.csv', index=False)
        same_locs.to_csv('SameLocs/samelocs_' + name + '.csv', index=False)
        self.performance.to_csv('Performance/performance_' + name + '.csv', index=False)
        return
    
    def performance_update(self, iters, score):
        if len(self.performance) == 0:
            old_iters = 0
        else:
            old_iters = self.performance.iloc[-1, :]['iters']
        self.performance = self.performance.append({'iters': iters + old_iters,'score': score}, ignore_index=True)
        return
        
    