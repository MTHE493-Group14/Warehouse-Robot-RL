import random

from warehouse_parameters import N_ROBOTS

class Actions:
    """
    The actions chosen by the central agent for all the robots to take.
    
    At any time step, each robot may move up, move down, move left, move right,
    lift a stack, or drop a stack.
    
    Attributes
    ----------
    valid_actions : [str]
        A list of the valid actions for a robot to take.
    actions : [str]
        A list containing 1 action for each of the robots to take. The length
        of actions is equal to N_ROBOTS.
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
        self.valid_actions = ['O', 'U', 'D', 'L', 'R', 'SU', 'SD', 'SL', 'SR']
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
        None.

        """
        ## RAISE EXCEPTION
        if robot_idx in range(N_ROBOTS) and action in self.valid_actions:
            self.actions[robot_idx] = action
        return
    
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
        None.

        """
        ## RAISE EXCEPTION
        if action in self.valid_actions:
            self.actions = [action] * N_ROBOTS
        return
        
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
            coeff = len(self.valid_actions)**(N_ROBOTS - 1 - i)
            enum += self.valid_actions.index(self.actions[i]) * coeff
        return enum
    
    def set_by_enum(self, num):
        num_acts = len(self.valid_actions)
        if num in range(num_acts ** N_ROBOTS):
            for i in range(N_ROBOTS):
                action_idx = int(num / num_acts**(N_ROBOTS - 1 - i)) % num_acts
                self.set_action(i, self.valid_actions[action_idx])
        return
    
    def __repr__(self):
        """
        Returns the string representation of an Actions object.

        Returns
        -------
        str
            The string representation of an Actions object.

        """
        return str(self.actions)