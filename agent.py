import copy
import random
import numpy as np

from actions import Actions
from tables import Tables
from performance import Performance
from warehouse_parameters import N_ROBOTS

class Agent:
    """
    The central agent that controls the actions of the robots.
    
    Attributes
    ----------
    tables : Tables
        The tables used for training.
    performance : Performance
        The dataframe tracking the performance of the greedy policy.
    """
    
    def __init__(self, filename, overwrite):
        """
        Creates an Agent object.
        
        The Agent chooses the actions to take according to some policy. It
        also keeps track of q-value estimates, visits, and which actions do 
        not change the robot/stack locations.
        
        Parameters
        ----------
        filename : str
            The filename that should be used to read/write the dataframe.
        overwrite : bool
            Whether or not the csvs should be overwritten by ones.

        Returns
        -------
        None.

        """
        self.tables = Tables(filename, overwrite)
        self.performance = Performance('tabular', filename, overwrite)
        return
    
    def min_visits_policy(self, current_state):
        """
        Selects the action that has been tried the least.

        Parameters
        ----------
        current_state : State
            The state the agent is currently in.

        Returns
        -------
        Actions
            The actions that should be taken if following this policy.

        """
        snum = current_state.enum()
        anum = np.argmin(self.tables.visits[snum])
        a = Actions()
        a.set_by_enum(anum)
        return a
    
    def greedy_policy(self, current_state):
        """
        Selects the action that has the lowest q-value estimate.

        Parameters
        ----------
        current_state : State
            The state the agent is currently in.

        Returns
        -------
        Actions
            The actions that should be taken if following this policy.

        """
        snum = current_state.enum()
        anum = np.argmin(self.tables.qvals[snum])
        a = Actions()
        a.set_by_enum(anum)
        return a

    def random_policy(self, current_state):
        """
        Randomly determines an action to take given the current state.

        Returns
        -------
        Actions
            The actions that should be taken if following this policy.

        """
        a = Actions()
        return a
    
    def epsilon_random_greedy_policy(self, current_state, epsilon):
        """
        Act randomly with probability epsilon. Otherwise act greedily.

        Parameters
        ----------
        current_state : State
            The current state the agent is in.
        epsilon : float
            The probability that the agent should act randomly.

        Returns
        -------
        Actions
            The actions that should be taken if following this policy.

        """
        if random.random() < epsilon:
            return self.random_policy(current_state)
        else:
            return self.greedy_policy(current_state)

    def epsilon_min_visits_greedy_policy(self, current_state, epsilon):
        """
        Choose least visited action with probability epsilon. Otherwise act greedily.

        Parameters
        ----------
        current_state : State
            The current state the agent is in.
        epsilon : float
            The probability that the agent should choose the least visited action.

        Returns
        -------
        Actions
            The actions that should be taken if following this policy.

        """
        if random.random() < epsilon:
            return self.min_visits_policy(current_state)
        else:
            return self.greedy_policy(current_state)
        
    def baseline_policy(self, current_state):
        """
        Determines what action to take in the current state if following the
        baseline_policy.
        
        In order to evaluate the policy learned by the reinforcement learning
        algorithm, we must compare the performance to the performance of 
        another policy. This baseline policy keeps all the stacks and robots 
        in the 2 middle rows until a stack needs to be returned to a picking 
        station.
        
        For each column in the grid, there are 2 stacks and 1 robot. The stack
        with the highest number of outstanding ordered items that is not 
        already at a picking station is identified. All robots will move to 
        the row that this desired stack is located, then the robot in the same 
        column as the desired stack will move the stack into one of the outer 
        rows (top or bottom row). The same robot will then move the desired 
        stack to the leftmost column in the grid (where the picking stations 
        are), and lastly the robot will return the desired stack to its 
        original row while the other robots shift the stacks to the right to 
        make room for the desired stack.
        
        When following this policy, there are 7 types of states. Each type of 
        state has a unique list of actions that should be taken when in that 
        type of state. The 7 cases are as follows:
        
        Case 1:
            All stacks and robots are in the 2 middle rows. Any stacks that do 
            have items ordered are already located at a picking station.
            
            In this type of state, nothing needs to be done. Each robot can 
            do nothing.
        Case 2:
            All stacks and robots are in the 2 middle rows. The robots are not
            in the same row as the stack with the most ordered items that is 
            not already at a picking station. 
            
            In this type of state, the robots need to move to the row with the 
            desired stack. Each robot should move up/down to the correct row.
        Case 3:
            All stacks and robots are in the 2 middle rows. The robots are in 
            the same row as the stack with the most ordered items that is not
            already at a picking station. 
            
            In this type of state, the robots are ready to start moving the 
            desired stack to a picking station. The robot in the same column
            as the desired stack should move the stack to an outer row. The 
            other robots can do nothing.
        Case 4: 
            All stacks and robots are in the 2 middle rows except for 1 robot 
            and stack. This robot and stack is heading down to the picking 
            station so the item can be collected by a worker but it has not 
            yet reached the leftmost column in the warehouse grid. All other 
            robots are waiting patiently in the desired stack's orginal row.
            
            In this type of state, the robots can continue moving the desired 
            stack to a picking station. The robot with the desired stack 
            should move left towards the picking stations while the others 
            continue to do nothing.
        Case 5:
            All stacks and robots are in the 2 middle rows except for 1 robot 
            and stack. This robot and stack is heading down to the picking 
            station so the item can be collected by a worker and has reached
            the leftmost column in the warehouse grid. All other robots are 
            waiting patiently in the desired stack's orginal row.
            
            In this type of state, the stacks in the original row can shift
            over with the stacks in their column to make room for the desired 
            stack to return to its original row. After this is done, the 
            desired stack will remain still in a picking station for a few 
            time steps so the worker can collect the ordered item. The robot 
            with the desired stack should move up/down to return to the 
            original row, any robots in columns that are to the left of the 
            desired stack's original column should move to the right with 
            their stacks to make room, and all other robots should do nothing.

        Returns
        -------
        a : Actions
            The list of actions that should be taken in the current state if 
            following the baseline policy.

        """
        ## RAISE EXCEPTION
        a = Actions()
        all_middle_rows = all([loc.row in {1, 2} for loc in current_state.robot_locs])
                    
        if all_middle_rows:
            orders = copy.deepcopy(current_state.orders)
            max_order = max(orders)
            desired_stack_idx = orders.index(max_order)
            desired_stack_loc = current_state.stack_locs[desired_stack_idx]
            while (desired_stack_loc.col == 0 and any(orders)):
                orders[desired_stack_idx] = 0
                max_order = max(orders)
                desired_stack_idx = orders.index(max_order)
                desired_stack_loc = current_state.stack_locs[desired_stack_idx]
            if max_order == 0 or desired_stack_loc.col == 0:
                # case 1
                a.set_all_actions('N')
            else:
                robot_cols = [loc.col for loc in current_state.robot_locs]
                desired_robot_idx = robot_cols.index(desired_stack_loc.col)
                if current_state.robot_locs[desired_robot_idx].row != desired_stack_loc.row:
                    # case 2
                    if desired_stack_loc.row == 1:
                        a.set_all_actions('U')
                    elif desired_stack_loc.row == 2:
                        a.set_all_actions('D')
                else:
                    # case 3
                    a.set_all_actions('N')
                    if desired_stack_loc.row == 1:
                        a.set_action(desired_robot_idx, 'SU')
                    elif desired_stack_loc.row == 2:
                        a.set_action(desired_robot_idx, 'SD')
        else:
            robot_cols = [loc.col for loc in current_state.robot_locs]
            in_outer_rows = [loc.row in {0, 3} for loc in current_state.robot_locs]
            desired_robot_idx = in_outer_rows.index(True)
            desired_robot_loc = current_state.robot_locs[desired_robot_idx]
            if desired_robot_loc.col > 0:
                # case 4
                a.set_all_actions('N')
                a.set_action(desired_robot_idx, 'SL')
            else:
                # case 5
                for robot_idx in range(N_ROBOTS):
                    if robot_idx not in robot_cols:
                        missing_col = robot_idx
                        break
                for robot_idx in range(N_ROBOTS):
                    robot_loc = current_state.robot_locs[robot_idx]
                    if robot_loc.col < missing_col:
                        a.set_action(robot_idx, 'SR')
                    else:
                        a.set_action(robot_idx, 'N')
                if desired_robot_loc.row == 0:
                    a.set_action(desired_robot_idx, 'SD')
                else:
                    a.set_action(desired_robot_idx, 'SU')
        return a