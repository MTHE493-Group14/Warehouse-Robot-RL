import numpy as np
import pandas as pd

from util import nCr
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, N_ITEMS, N_ACTIONS, DISCOUNT

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
    """
    
    def __init__(self, filename, overwrite):
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

        Parameters
        ----------
        filename : str
            The filename that should be used to read in csvs.
        overwrite : bool
            Whether the tables should be overwritten by new ones.

        Returns
        -------
        None.

        """
        if overwrite:
            num_states = (nCr(N_ROWS*N_COLS+1, N_ROBOTS) 
                          * nCr(N_ROWS*N_COLS+1, N_STACKS)    
                          * (N_ITEMS+1)**N_STACKS)
            num_actions = N_ACTIONS**N_ROBOTS
            
            self.qvals = np.ones((num_states, num_actions)) * (N_ROWS + N_COLS - 1) * N_STACKS
            self.visits = np.zeros((num_states, num_actions))
            self.same_locs = np.concatenate((np.ones((num_states, 1)), 
                                             np.zeros((num_states, num_actions-1))), 
                                            axis=1)
            self.save(filename)
        else:
            qvals = pd.read_csv('Q-Tables/qtable_' + filename + '.csv')
            visits = pd.read_csv('Visits/visits_' + filename + '.csv')
            same_locs = pd.read_csv('SameLocs/samelocs_' + filename + '.csv')
        
            self.qvals = np.asarray(qvals)
            self.visits = np.asarray(visits)
            self.same_locs = np.asarray(same_locs)
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
            alpha = 1 / (self.visits[s1num][anum] + 1)
            self.qvals[s1num][anum] += alpha*(c + DISCOUNT*(min_val) - old_val)
            self.visits[s1num][anum] += 1
        else:
            # vectorize updates using numpy arrays
            self.same_locs[s1num][a.enum()] = 1
            anums = np.argwhere(self.same_locs[s1num] == 1).flatten()
            old_vals = self.qvals[s1num][anums]
            min_val = min(self.qvals[s2num])
            alpha = 1 / (self.visits[s1num][anums] + 1)
            self.qvals[s1num][anums] += alpha*(c + DISCOUNT*(min_val) - old_vals)
            self.visits[s1num][anums] += 1
        return

    def get_greedy_actions(self):
        return np.argmin(self.qvals, axis=1)
    
    def save(self, filename):
        """
        Save the tables to use again later on.
        
        Convert the NumPy Arrays to Pandas DataFrames and save these as csvs.

        Parameters
        ----------
        filename : str
            The filename that should be used to save the tables as csvs.
        
        Returns
        -------
        None.

        """
        
        qvals = pd.DataFrame(self.qvals)
        visits = pd.DataFrame(self.visits)
        same_locs = pd.DataFrame(self.same_locs)
        
        qvals.to_csv('Q-Tables/qtable_' + filename + '.csv', index=False)
        visits.to_csv('Visits/visits_' + filename + '.csv', index=False)
        same_locs.to_csv('SameLocs/samelocs_' + filename + '.csv', index=False)
        return
        
    