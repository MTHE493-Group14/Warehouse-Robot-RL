import random
import numpy as np
import pandas as pd

from warehouse_parameters import N_ROBOTS, N_ACTIONS

class Actions:
    """
    The actions that the robots will take, chosen by the central agent.
    
    At any time step, each robot may perform one of the following 9 actions:
        N : Do nothing.
        U : Move up.
        D : Move down.
        L : Move left.
        R : Move right.
        SU : Move up with a stack.
        SD : Move down with a stack.
        SL : Move left with a stack.
        SR : Move right with a stack.
    
    Attributes
    ----------
    valid_actions : [str]
        A list of the valid actions for a robot to take. This list does not 
        change.
    actions : [str]
        A list containing 1 action per robot. The length of actions is equal 
        to N_ROBOTS.
    """
    
    def __init__(self):
        """
        Creates a new Actions object.
        
        When an Actions object is initialized, random actions for each robot 
        are chosen. However, these actions may be changed using the set_action
        and set_all_actions methods.

        Returns
        -------
        None.

        """
        self.valid_actions = ['N', 'U', 'D', 'L', 'R', 'SU', 'SD', 'SL', 'SR']
        self.actions = random.choices(self.valid_actions, k=N_ROBOTS)
        return
    
    def set_action(self, robot_idx, action):
        """
        Sets the action of one robot.
        
        The robot_idx must be a valid index and the action must be a valid 
        action.

        Parameters
        ----------
        robot_idx : int
            The index of the robot whose action is being set.
        action : str
            The action that is being set.

        Returns
        -------
        bool
            Boolean value indicating if the action was successfully set.

        """
        ## RAISE EXCEPTION
        if robot_idx in range(N_ROBOTS):
            if action in self.valid_actions:
                self.actions[robot_idx] = action
                return True
            else:
                print('Error: ' + action + ' is not a valid action.')
                return False
        else:
            print('Error: ' + str(robot_idx) + ' is not a valid robot index.')
            return False
    
    def set_all_actions(self, action):
        """
        Sets the actions of all robots to all be the same action.
        
        The action must be a valid action.

        Parameters
        ----------
        action : str
            The action that is being set.

        Returns
        -------
        bool
            Boolean value indicating if the action was successfully set.

        """
        ## RAISE EXCEPTION
        if action in self.valid_actions:
            self.actions = [action] * N_ROBOTS
            return True
        else:
            print('Error: ' + action + ' is not a valid action.')
            return False
        
    def enum(self):
        """
        Enumerates the list of actions.
        
        This method will be useful when for the Q-table when Q-learning is 
        implemented.
        
        For each action, multiply the action number by the number of possible
        actions the remaining robots could take.
        
        Returns
        -------
        int
            The enumeration of the list of actions.

        """
        enum = 0
        for i in range(N_ROBOTS):
            coeff = N_ACTIONS**(N_ROBOTS - 1 - i)
            enum += self.valid_actions.index(self.actions[i]) * coeff
        return enum
    
    def set_by_enum(self, num):
        """
        Set the action according to an enumeration value.

        Parameters
        ----------
        num : int
            Enumeration value.

        Returns
        -------
        bool
            Boolean value indicating if the action was successfully set.

        """
        if num in range(N_ACTIONS ** N_ROBOTS):
            for i in range(N_ROBOTS):
                action_idx = int(num / N_ACTIONS**(N_ROBOTS - 1 - i)) % N_ACTIONS
                self.set_action(i, self.valid_actions[action_idx])
            return True
        else:
            return False
        
    def features(self):
        """
        Return the features values for actions.

        Returns
        -------
        [int]
            A list of feature values.

        """
        a = pd.Series(self.actions).str
        f = np.concatenate((a.count('N'),
                            a.count('U'), 
                            a.count('D'), 
                            a.count('L'), 
                            a.count('R'), 
                            a.count('S')), axis=None)
        return f

    def features2(self):
        anums = [self.valid_actions.index(a) for a in self.actions]
        f = np.zeros((N_ROBOTS, N_ACTIONS), dtype=int)
        f[np.arange(N_ROBOTS), anums] = 1
        return f.flatten()
    
    def __repr__(self):
        """
        Returns the string representation of an Actions object.

        Returns
        -------
        str
            The string representation of an Actions object.

        """
        return str(self.actions)