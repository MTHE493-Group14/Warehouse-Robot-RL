import random
import math
import copy

"""
Created by Adam Farley, Daniel Molyneaux, Ian Ho, and Sang Park for MTHE 493.
Last updated: January 2021

This script will simulate the movements of Amazon warehouse robots as they
move items around an Amazon warehouse. 

The warehouse is represented as a grid with robots and inventory stacks 
occupying cells in the grid. The initial locations of the robots and stacks 
will follow a uniform distribution. At each time step, the environment will
determine which items are ordered, a central agent will decide which actions 
each robot should take, and the total accumulated cost will be updated.

Each inventory stack will contain 10 items. At the beginning of each time step,
each item has a 0.1% chance of being ordered by an Amazon customer.

Picking stations will be located in the first column of the warehouse grid. 
The robots must deliver the inventory stacks containing the ordered items to 
the picking stations. When an inventory stack with an ordered item stays in a 
picking station for 1 time step. The picking station workers will be able to 
collect the ordered item and replace the item on that stack with a new item.

Each warehouse robots my take any of the following 6 actions at each time 
step: move up, move down, move left, move right, pick up an inventory stack, 
or drop an inventory stack. Some actions may not be available in certain 
states (e.g. if a robot is in the top row of the grid, they may not move up).

"""


N_ITER = 100
POLICY_TYPE = 'random'

N_ROWS = 4
N_COLS = 6
N_ROBOTS = 5
N_STACKS = 10
ORDER_PROB = 0.05




class Location:
    """
    Location objects represent the grid coordinates of a warehouse robot or 
    inventory stack.
    
    Attributes
    ----------
    row : int
        The row of the cell that the robot or stack is located in.
    col : int
        The column of the cell that the robot or stack is located in.
    
    """
    
    def __init__(self, row, col):
        """
        Creates a new Location object given a set of coordinates.

        Parameters
        ----------
        row : int
            The row of the cell that the robot or stack is located in.
        col : int
            The column of the cell that the robot or stack is located in.

        Returns
        -------
        None.

        """
        self.row = row
        self.col = col
        return
    
    def __eq__(self, other):
        """
        Given another Location object, determine if the locations are the same.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indication if the locations are equal.

        """
        return self.row == other.row and self.col == other.col
    
    def __repr__(self):
        """
        Return the string representation of a Location object. 

        Returns
        -------
        str
            The string representation of a Location object.

        """
        return "(" + str(self.row) + ", " + str(self.col) + ")"

    
    
    


        
class State:
    """
    The state of the environment.
    
    The state of the environment encodes the locations of the robots, the 
    locations of the stacks, which robots are carrying stacks, and how many 
    items on each stack have already been ordered by Amazon customers. The 
    state is used by the agent to determine which action to take.
    
    Attributes
    ----------
    robot_locs : [Location]
        The locations of each of the robots. The length of robot_locs is equal 
        to N_ROBOTS.
    stack_locs : [Location]
        The locations of each of the stacks. The length of stack_locs is equal
        to N_STACKS.
    lift : [bool]
        Which of the robots are lifting stacks. The length of lift is equal 
        to N_ROBOTS.
    num_ordered : [int]
        The number of ordered items that each stack contains. The length of 
        num_ordered is equal to N_STACKS.
    
    """
    
    def __init__(self):
        """
        Creates a new State object. 
        
        The initial locations of the robots and stacks are random (follow a 
        discrete uniform distribution). Initally, none of the robots are 
        carrying stacks and none of the items on the stacks have been ordered 
        yet.

        Returns
        -------
        None.

        """
        # create list of all possible locations in the warehouse grid
        location_indices = list(range(N_ROWS * N_COLS))
        idx_to_loc = lambda i: Location(math.floor(i / N_COLS), i % N_COLS)
        locations = list(map(idx_to_loc, location_indices))
        
        self.robot_locs = random.sample(locations, k=N_ROBOTS)
        self.stack_locs = random.sample(locations, k=N_STACKS)
        self.lift = [False]* N_ROBOTS
        self.num_ordered = [0]* N_STACKS
        return
    
    def organize_in_rows(self):
        """
        Initializes robot and stack locations for the baseline policy.
        
        The baseline policy requires that the stacks are located in the middle
        2 rows of the warehouse grid and the robots are located in one of 
        those 2 middle rows in the grid. This method must be called before 
        using the baseline policy.
        
        The method assumes that the warehouse is a 4x6 grid and that there are
        5 robots and 10 stacks in the warehouse.

        Returns
        -------
        None.

        """
        ### RAISE EXCEPTION
        if (N_ROWS == 4 and N_STACKS == 2*N_ROBOTS and N_COLS >= N_ROBOTS
            and POLICY_TYPE == 'baseline'):
            self.robot_locs = [Location(1, i) for i in range(N_ROBOTS)]
            self.stack_locs = ([Location(1, i) for i in range(N_ROBOTS)] 
                               + [Location(2, i) for i in range(N_ROBOTS)])
        return
    
        
    def enumerate_state():
        """
        Assigns a number to a particular state.
        
        This method will be useful when for the Q-table when Q-learning is 
        implemented.
        
        NOT COMPLETE

        Returns
        -------
        None.

        """
        pass
    
    def __repr__(self):
        """
        Returns the string representation of a State object.

        Returns
        -------
        s : str
            The string representation of a State object.

        """
        s = ""
        for i in range(N_ROWS):
            s += "\n" + "-" * 6 * N_COLS + "---\n|"
            for j in range(N_COLS):
                loc = Location(i, j)
                cell = " "
                if loc in self.robot_locs:
                    if self.lift[self.robot_locs.index(loc)]:
                        cell += "R "
                    else:
                        cell += "r "
                else:
                    cell += "  "
                    
                if loc in self.stack_locs:
                    if self.num_ordered[self.stack_locs.index(loc)] > 0:
                        cell += "$"
                    else:
                        cell += "s"
                else:
                    cell += " "
                    
                if j == 0:
                    s += "|" + cell + " ||"
                else:
                    s += cell + " |"
        s += "\n" + "-" * 6 * N_COLS + "---\n"
        s += "robots = " + str(self.robot_locs) + '\n'
        s += "stacks = " + str(self.stack_locs) + '\n'
        s += "lifting = " + str(self.lift) + '\n'
        s += "ordered = " + str(self.num_ordered) + '\n'
        return s



    
    
    
    
class Actions:
    """
    The actions chosen by the central agent for all the robots to take.
    
    At any time step, each robot may move up, move down, move left, move right,
    lift a stack, or drop a stack.
    
    Attributes
    ----------
    valid_actions : [str]
        The 6 actions that are valid for a single robot to take. These actions
        are denoted by the strings: 'U', 'D', 'L', 'R', 'lift', and 'drop'.
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
        self.valid_actions = ['U', 'D', 'L', 'R', 'lift', 'drop']
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
        
    def enumerate_actions():
        """
        Assigns a number to a particular set of actions.
        
        This method will be useful when for the Q-table when Q-learning is 
        implemented.
        
        NOT COMPLETE

        Returns
        -------
        None.

        """
        pass
    
    def __repr__(self):
        """
        Returns the string representation of an Actions object.

        Returns
        -------
        str
            The string representation of an Actions object.

        """
        return self.actions
    
    
    
    
    
    
class Agent:
    """
    The central agent that controls the actions of the robots.
    
    """
    
    def __init__(self):
        """
        Creates an Agent object.
        
        The agent may follow a random policy, baseline policy, learning policy,
        or optimal policy.

        Returns
        -------
        None.

        """
        return
    
    def policy(self, current_state):
        """
        Determines the action that the agent should take in the current state.
        
        The policy used depends on the policy_type attribute.

        Parameters
        ----------
        current_state : State
            The current state of the environment.

        Returns
        -------
        a : Actions
            The set of actions to take in the current state.

        """
        if POLICY_TYPE == 'baseline':
            a = self.baseline_policy(current_state)
        else:
            a = self.random_policy(current_state)
        return a
    
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
        with the highest number of outstanding ordered items is identified.
        All robots will move to the correct row that this stack is located, 
        then the robot in the same column as the desired stack will move the 
        stack into one of the outer rows (top or bottom row), the same robot 
        will then move the desired stack to the leftmost column in the grid 
        (where the picking stations are), and lastly the robot will return the 
        desired stack to its original row while the other robots shift the 
        stacks to the right to make room for the desired stack.
        
        When following this policy, there are 7 types of states. Each type of 
        state has a unique set of actions that should be taken when in that 
        type of state. The 7 cases are as follows:
        
        Case 1:
            All stacks and robots are in the 2 middle rows. Any stacks that do 
            have items ordered are already located at a picking station.
            
            In this type of state, nothing needs to be done. Each robot can 
            perform the 'drop' action.
        Case 2:
            All stacks and robots are in the 2 middle rows. The robots are
            lifting stacks in one of the rows but the stack with the most 
            ordered items that is not already located at a picking 
            station is in the other row.
            
            In this type of state, the robots need to prepare to move to the 
            row with the desired stack. Each robot should drop the stacks they 
            are lifting.
        Case 3:
            All stacks and robots are in the 2 middle rows. The robots are
            not lifting stacks but the stack with the most ordered items that 
            is not already located at a picking station is in the other row.
            
            In this type of state, the robots are ready to move to the correct 
            row with the desired stack. Each robot should move up/down to be 
            in the correct row.
        Case 4:
            All stacks and robots are in the 2 middle rows. The robots are
            not lifting stacks and the stack with the most ordered items that 
            is not already located at a picking station is in the same row as
            the robots.
            
            In this type of state, the robots are ready to pick up the desired
            stack and start moving it to a picking station. Each robot should 
            lift the stack in the same location as them.
        Case 5:
            All stacks and robots are in the 2 middle rows. The robots are 
            lifting stacks, including the stack with the most ordered items 
            that is not already located at a picking station.
            
            In this type of state, the robots are ready to start moving the 
            desired stack to a picking station. The robot lifting the desired 
            stack should move up/down into an outer row while the others 
            continue to lift their stacks.
        Case 6: 
            All stacks and robots are in the 2 middle rows except for 1 robot 
            and stack. This robot and stack is heading down to the picking 
            station so the item can be collected by a worker but it has not 
            yet reached the first column in the warehouse grid. All other 
            robots are still lifting stacks in the desired stack's orginal 
            row.
            
            In this type of state, the robots can continue moving the desired 
            stack to a picking station. The robot lifting the desired stack 
            should move left towards the picking stations while the others 
            continue to lift their stacks.
        Case 7:
            All stacks and robots are in the 2 middle rows except for 1 robot 
            and stack. This robot and stack is heading down to the picking 
            station so the item can be collected by a worker and has reached
            the first column in the warehouse grid. All other robots are still 
            lifting stacks in the desired stack's orginal row.
            
            In this type of state, the stacks in the original row can shift
            over to make room for the desired stack to return to its original 
            row. After this is done, the desired stack will remain still in 
            a picking station for a few time steps so the worker can collect
            the ordered item. The robot lifting the desired stack should move 
            up/down to return to the original row, any robots in columns that
            are to the left of the desired stack's original column should 
            move to the right to make room, and all other robots should 
            continue to lift their stacks.

        Returns
        -------
        a : Actions
            The set of actions that should be taken in the current state if 
            following the baseline policy.

        """
        ## RAISE EXCEPTION
        a = Actions()
        all_middle_rows = all([loc.row in {1, 2} for loc in current_state.robot_locs])
                    
        if all_middle_rows:
            orders = copy.deepcopy(current_state.num_ordered)
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
                a.set_all_actions('drop')
            else:
                robot_cols = [loc.col for loc in current_state.robot_locs]
                desired_robot_idx = robot_cols.index(desired_stack_loc.col)
                if current_state.robot_locs[desired_robot_idx].row != desired_stack_loc.row:
                    if current_state.lift[desired_robot_idx]:
                        # case 2
                        a.set_all_actions('drop')
                    else:
                        # case 3
                        if desired_stack_loc.row == 1:
                            a.set_all_actions('U')
                        elif desired_stack_loc.row == 2:
                            a.set_all_actions('D')
                else:
                    if not current_state.lift[desired_robot_idx]:
                        # case 4
                        a.set_all_actions('lift')
                    else:
                        # case 5
                        a.set_all_actions('lift')
                        if desired_stack_loc.row == 1:
                            a.set_action(desired_robot_idx, 'U')
                        elif desired_stack_loc.row == 2:
                            a.set_action(desired_robot_idx, 'D')
        else:
            robot_cols = [loc.col for loc in current_state.robot_locs]
            in_outer_rows = [loc.row in {0, 3} for loc in current_state.robot_locs]
            desired_robot_idx = in_outer_rows.index(True)
            desired_robot_loc = current_state.robot_locs[desired_robot_idx]
            if desired_robot_loc.col > 0:
                # case 6
                a.set_all_actions('lift')
                a.set_action(desired_robot_idx, 'L')
            else:
                # case 7
                for robot_idx in range(N_ROBOTS):
                    if robot_idx not in robot_cols:
                        missing_col = robot_idx
                        break
                for robot_idx in range(N_ROBOTS):
                    robot_loc = current_state.robot_locs[robot_idx]
                    if robot_loc.col < missing_col:
                        a.set_action(robot_idx, 'R')
                    else:
                        a.set_action(robot_idx, 'lift')
                if desired_robot_loc.row == 0:
                    a.set_action(desired_robot_idx, 'D')
                else:
                    a.set_action(desired_robot_idx, 'U')
        return a
    
    def random_policy(self, current_state):
        """
        Randomly determines an action to take given the current state.
        
        This policy is only used to test the functionality of the simulation.
        
        First, a random set of actions is selected, the new state is 
        calculated given that random set of actions, and then it is checked if
        the new state is possible. If the new state is possible, return that 
        set of actions. If the new state is not possible, the process is 
        repeated until a set of actions is found that results in a possible 
        new state.

        Returns
        -------
        Actions
            A set of actions that is possible in the current state.

        """
        possibleState = False
        while not possibleState:
            a = Actions()
            new_state = self.calculate_state(current_state, a)
            possibleState = self.possible_state(current_state, new_state)
        return a
    
    def calculate_state(self, current_state, a):
        """
        Determines the new state if taking an action in the current state. 
        
        For each robot, check if there stack in the same location as the 
        robot and then make adjustments to the state based on what the action
        is. Next, check if stacks are located in the picking stations and 
        adjust the number of ordered items on the stacks accordingly.
        
        If the action is to move up, down, left or right, then adjust the 
        location of the robot. If there is a stack in the same location as the 
        robot and the robot is lifting the stack, then the stack will move 
        along with the robot. If not, then only the robot will move.
        
        If the action is to lift a stack, the lift state for that robot will 
        be set to True if there is a stack in the same location as the robot.
        
        If the action is to drop a stack, then the lift state for that robot 
        will be set to False.
        
        If a stack remains in a picking station for 1 whole time step, then if 
        the stack has ordered items, the num_ordered value for that stack will
        decrease by 1. Note: it does not matter if there is a robot carrying 
        stack or not, as long as the stack remains in the same location at a
        picking station, it is assumed that the item can be collected.

        Parameters
        ----------
        current_state : State
            The current state of the environment.
        a : Actions
            The action that the agent will take.

        Returns
        -------
        new_state : State
            The new state that the environment will enter if the given action
            is taken.

        """
        new_state = copy.deepcopy(current_state)

        for robot_idx in range(N_ROBOTS):
            try:
                stack_num = current_state.stack_locs.index(current_state.robot_locs[robot_idx])
            except ValueError:
                stack_num = -1 # there is no stack in the same location
            lifting = current_state.lift[robot_idx]

            if a.actions[robot_idx] == "U":
                new_state.robot_locs[robot_idx].row -= 1
                if stack_num != -1 and lifting:
                    new_state.stack_locs[stack_num].row -= 1
            elif a.actions[robot_idx] == "D":
                new_state.robot_locs[robot_idx].row += 1
                if stack_num != -1 and lifting:
                    new_state.stack_locs[stack_num].row += 1
            elif a.actions[robot_idx] == "L":
                new_state.robot_locs[robot_idx].col -= 1
                if stack_num != -1 and lifting:
                    new_state.stack_locs[stack_num].col -= 1
            elif a.actions[robot_idx] == "R":
                new_state.robot_locs[robot_idx].col += 1
                if stack_num != -1 and lifting:
                    new_state.stack_locs[stack_num].col += 1
            elif a.actions[robot_idx] == "lift":
                if stack_num != -1:
                    new_state.lift[robot_idx] = True
            elif a.actions[robot_idx] == "drop":
                new_state.lift[robot_idx] = False
            else:
                ## RAISE EXCEPTION
                print("Error: Invalid action")
                
        for stack_idx in range(N_STACKS):
            if (current_state.stack_locs[stack_idx] == new_state.stack_locs[stack_idx] 
                and new_state.stack_locs[stack_idx].col == 0):
                new_state.num_ordered[stack_idx] = max(new_state.num_ordered[stack_idx] - 1, 0)
        return new_state
    
    def possible_state(self, current_state, new_state):
        """
        Checks if it is possible to transition from the current state to 
        the given new state.
        
        First, it is checked that no robot leaves the warehouse grid in the
        new state and that no two robots are in the same location in the new
        state. Next, it is checked that no stack leaves and warehouse grid in 
        new state and that no two stacks are in the same location in the new 
        state. Lastly, it is checked that no two robots pass through one 
        another when transitioning from the current state to the new state 
        (i.e. 2 robots switch locations in the transition).
        
        If all these conditions are met, then the new state is possible. If 
        not, then the new state is not possible.

        Parameters
        ----------
        current_state : State
            The current state of the environment.
        new_state : State
            The new state that will be transitioned to from the current state.

        Returns
        -------
        bool
            A boolean value indicating if the state transition is possible.

        """
        robot_locs_taken = []
        for robot_loc in new_state.robot_locs:
            if (robot_loc.row in list(range(N_ROWS))
                and robot_loc.col in list(range(N_COLS))
                and robot_loc not in robot_locs_taken):
                robot_locs_taken.append(robot_loc)
            else: 
                return False
                
        stack_locs_taken = []
        for stack_loc in new_state.stack_locs:
            if (stack_loc.row in list(range(N_ROWS))
                and stack_loc.col in list(range(N_COLS))
                and stack_loc not in stack_locs_taken):
                stack_locs_taken.append(stack_loc)
            else: 
                return False
        
        robot_locs1 = current_state.robot_locs
        robot_locs2 = new_state.robot_locs
        for i in range(N_ROBOTS):
            for j in range(N_ROBOTS):
                if (robot_locs1[i] == robot_locs2[j] 
                    and robot_locs2[i] == robot_locs1[j] 
                    and i != j):
                    return False
        return True





    
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
    total_orders : int
        The total number of orders throughout the simulation.
    total_returns : int
        The total number of items ordered by Amazon customers that have been 
        returned to the workers in the picking stations.
    """
    
    def __init__(self):
        self.state = State()
        if POLICY_TYPE == 'baseline':
            self.state.organize_in_rows()
        self.agent = Agent()
        self.cost = 0
        self.total_orders = 0
        self.total_returns = 0
        return
    

    def order_items(self):
        """
        Determines if more items are ordered.
        
        At the beginning of each time step, the environment must check if more
        items are ordered. For each stack, it compares a random number in the 
        interval (0,1) to the probability that another item on that stack will
        be ordered. If the random number is less than the order probability, 
        the number of ordered items on that stack will increase by 1 unless 
        there is already 10 ordered items on the stack.

        Returns
        -------
        None.

        """
        for i in range(N_STACKS):
            if random.random() < ORDER_PROB:
                if self.state.num_ordered[i] < 10:
                    self.state.num_ordered[i] += 1
                    self.total_orders += 1
        return
        
    
    
    def update_cost(self):
        """
        Updates the total accumulated cost since the start of the simulation.
        
        The cost is the sum of the number of time steps between an item being 
        ordered and it being collected by a picking station worker.

        Returns
        -------
        None.

        """
        self.cost += sum(self.state.num_ordered)
        return
    
        
    def __repr__(self):
        """
        Returns the string representation of an Environment object.

        Returns
        -------
        str
            The string representation of an Environment object.

        """
        return (str(self.state)
                + "cost = " + str(self.cost) 
                + ", total_orders = " + str(self.total_orders) 
                + ", total_returns = " + str(self.total_returns))








def main():
    env = Environment()
    
    for time_step in range(N_ITER):
        print("\n\nt = " + str(time_step))
        env.order_items()
        print(env)
        a = env.agent.policy(env.state)
        print("actions = " + str(a.actions))
        
        num_ordered1 = sum(env.state.num_ordered)
        env.state = env.agent.calculate_state(env.state, a)
        num_ordered2 = sum(env.state.num_ordered)
        env.total_returns += num_ordered1 - num_ordered2
        env.update_cost()
    return

main()







