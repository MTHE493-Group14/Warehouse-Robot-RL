import copy
import random

from location import Location
from state import State
from agent import Agent
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, N_ITEMS, ORDER_PROB

class Environment():
    """
    The warehouse environment that the agent is interacting with.
    
    Attributes
    ----------
    state : State
        The current state of the environment that the agent bases its 
        decisions off of.
    agent : Agent
        The agent that is interacting with the environment.
    cost : int
        The total accumulated cost throughout the simulation.
    """
    
    def __init__(self):
        """
        Initialize the environment by initializing the state, agent, and cost.

        Returns
        -------
        None.

        """
        self.state = State()
        self.agent = Agent()
        self.cost = 0
        return
    
    def calculate_state(self, current_state, a):
        """
        Determines the new state if taking an action in the current state. 
        
        For each robot, check if there stack in the same location as the 
        robot and then make adjustments to the state based on what the action
        is. Do not allow the robots/stacks to leave the grid.
        
        Check if any two robots are in the same spot or if any two robots
        passed through one another. If either of these things occurred reset 
        the robot/stack locations to the original locations.
        
        Determine if any new items were ordered. For each stack, generate a 
        random number and see if that number is less than the order 
        probability. If it is, increase the orders value that stack by 1. 
        
        Determine if any ordered items were returned. If a stack remains in a 
        picking station for 1 whole time step, then it is assumed that a 
        picking station worker can collect that item and the orders value for 
        that stack will decrease by 1. 
        
        Lastly, reorder the lists in the state so that the locations are in
        ascending order.

        Parameters
        ----------
        current_state : State
            The current state of the environment.
        a : Actions
            The action that the agent will take.

        Returns
        -------
        State
            The new state that the environment will enter if the given action
            is taken.

        """
        # determine new robot and stack locations
        new_state = copy.deepcopy(current_state)
        robot_locs = copy.deepcopy(current_state.robot_locs)
        
        for robot_idx in range(N_ROBOTS):
            row = robot_locs[robot_idx].row
            col = robot_locs[robot_idx].col
            
            if robot_locs[robot_idx] in current_state.stack_locs:
                stack_num = current_state.stack_locs.index(robot_locs[robot_idx])
            else:
                stack_num = -1
                

            if a.actions[robot_idx] == "U":
                new_state.robot_locs[robot_idx] = Location(max(row-1, 0), col)
            elif a.actions[robot_idx] == "SU" and stack_num != -1:
                new_state.robot_locs[robot_idx] = Location(max(row-1, 0), col)
                new_state.stack_locs[stack_num] = Location(max(row-1, 0), col)
            elif a.actions[robot_idx] == "D":
                if col > -1:
                    new_state.robot_locs[robot_idx] = Location(min(row+1, N_ROWS-1), col)
            elif a.actions[robot_idx] == "SD" and stack_num != -1:
                if col > -1:
                    new_state.robot_locs[robot_idx] = Location(min(row+1, N_ROWS-1), col)
                    new_state.stack_locs[stack_num] = Location(min(row+1, N_ROWS-1), col)
            elif a.actions[robot_idx] == "L":
                if row == 0:
                    new_state.robot_locs[robot_idx] = Location(row, max(col-1, -1))
                else:
                    new_state.robot_locs[robot_idx] = Location(row, max(col-1, 0))
            elif a.actions[robot_idx] == "SL" and stack_num != -1:
                if row == 0:
                    new_state.robot_locs[robot_idx] = Location(row, max(col-1, -1))
                    new_state.stack_locs[stack_num] = Location(row, max(col-1, -1))
                else:
                    new_state.robot_locs[robot_idx] = Location(row, max(col-1, 0))
                    new_state.stack_locs[stack_num] = Location(row, max(col-1, 0))
            elif a.actions[robot_idx] == "R":
                new_state.robot_locs[robot_idx] = Location(row, min(col+1, N_COLS-1))
            elif a.actions[robot_idx] == "SR" and stack_num != -1:
                new_state.robot_locs[robot_idx] = Location(row, min(col+1, N_COLS-1))
                new_state.stack_locs[stack_num] = Location(row, min(col+1, N_COLS-1))
        
        possible = True
        
        # check if 2 robots or stacks are in the same spot
        if (len(set(new_state.robot_locs)) < N_ROBOTS 
            or len(set(new_state.stack_locs)) < N_STACKS):
            possible = False
            new_state.robot_locs = copy.deepcopy(current_state.robot_locs)
            new_state.stack_locs = copy.deepcopy(current_state.stack_locs)

        # check if robots passed through one another
        for i in range(N_ROBOTS):
            if not possible:
                break
            else:
                for j in range(N_ROBOTS):
                    if (robot_locs[i] == new_state.robot_locs[j] 
                        and new_state.robot_locs[i] == robot_locs[j] 
                        and i != j):
                            possible = False
                            new_state.robot_locs = copy.deepcopy(current_state.robot_locs)
                            new_state.stack_locs = copy.deepcopy(current_state.stack_locs)
                            break
        
        # check for new orders and determine if items were returned
        order_nums = copy.deepcopy(new_state.orders)
        for stack_idx in range(N_STACKS):
            if random.random() < ORDER_PROB:
                new_state.orders[stack_idx] = min(order_nums[stack_idx] + 1, N_ITEMS)
            if (current_state.stack_locs[stack_idx] == new_state.stack_locs[stack_idx] 
                and new_state.stack_locs[stack_idx].col == -1):
                new_state.orders[stack_idx] = max(order_nums[stack_idx] - 1, 0)
        
        
        # reorder robots and stacks
        new_state.orders = [order_num for _, order_num in sorted(zip(new_state.stack_locs, new_state.orders))]
        new_state.robot_locs.sort()
        new_state.stack_locs.sort()
            
        return new_state
    
    
    def update_cost(self):
        """
        Updates the total accumulated cost since the start of the simulation.
        
        The cost is increased by the number of items that have not been 
        returned.

        Returns
        -------
        None.

        """
        self.cost += sum(self.state.orders)
        return
    
        
    def __repr__(self):
        """
        Returns the string representation of an Environment object.

        Returns
        -------
        str
            The string representation of an Environment object.

        """
        return str(self.state) + "cost = " + str(self.cost)