import random
import math
import copy

from location import Location
from util import nCr
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, N_ITEMS

class State:
    """
    The state of the environment.
    
    The state of the environment contains a list of the locations of the 
    robots, a list of the locations of the stacks, and a list of integers that
    indicate the number of items on each stack that have been ordered by 
    Amazon customers. The state is used by the agent to determine which action 
    to take.
    
    To reduce the size of the state space, we group together all states where 
    the robot/stack locations are the same but are ordered differently. To
    implement this grouping, anytime the robot/stack locations are changed, we
    reorder the lists contained in the state object so that the locations are 
    in ascending order. 
    
    For example, consider if we had the following state:
        
        robot_locs = [(0,1), (1,1), (1,0)]
        stack_locs = [(0,1), (1,0), (0,0)]
        orders = [1, 0, 1]
        
    The robot_locs list would be reordered by switching the order of the last 
    two locations. The stack_locs list would be reordered by moving the last 
    location to the front of the list. Since the orders list contains numbers 
    that correspond to particular stacks, the orders list should be reordered
    by performing the same rearrangements that the stack_locs list made 
    instead of reordering the list based on the integers it contains. 
    
    Our resulting state would be as follows:
        
        robot_locs = [(0,1), (1,0), (1,1)]
        stack_locs = [(0,0), (0,1), (1,0)]
        orders = [1, 1, 0]
    
    Attributes
    ----------
    robot_locs : [Location]
        The locations of each of the robots. The locations in robot_locs are 
        always in ascending order. The length of robot_locs is equal to 
        N_ROBOTS.
    stack_locs : [Location]
        The locations of each of the stacks. The locations in stack_locs are
        always in ascending order. The length of stack_locs is equal to 
        N_STACKS.
    orders : [int]
        The number of ordered items that each stack contains. Each value in 
        orders cannot be any larger than N_ITEMS. The length of orders 
        is equal to N_STACKS.
    
    """
    
    def __init__(self):
        """
        Creates a new State object. 
        
        Call the reset() method to initialize robot/stack locations and set 
        the number of ordered items on each stack to 0. 

        Returns
        -------
        None.

        """
        self.reset()
        return
    
    def reset(self):
        """
        Assign random new locations to the robots and stacks based on a 
        discrete uniform distribution. Reorder the locations to be in 
        ascending order. Set the number of ordered items for each stack to 0.

        Returns
        -------
        None.

        """
        map_idx_to_loc = lambda i: Location(math.floor(i / N_COLS), i % N_COLS)
        valid_locations = list(map(map_idx_to_loc, range(N_ROWS * N_COLS)))
        self.robot_locs = random.sample(valid_locations, k=N_ROBOTS)
        self.robot_locs.sort()
        self.stack_locs = random.sample(valid_locations, k=N_STACKS)
        self.stack_locs.sort()
        self.orders = [0]* N_STACKS
        return
    
    
    def baseline_organization(self):
        """
        Initializes robot and stack locations for the baseline policy.
        
        The baseline policy requires that the stacks are located in the middle
        2 rows of the warehouse grid and the robots are located in one of 
        those 2 middle rows in the grid. This method must be called before 
        using the baseline policy.
        
        The method assumes that the warehouse has at least 4 rows, at least as 
        many columns as robots, and twice as many stacks as robots.

        Returns
        -------
        None.

        """
        ### RAISE EXCEPTION
        if (N_ROWS >= 4 and N_COLS >= N_ROBOTS and N_STACKS == 2*N_ROBOTS):
            self.robot_locs = [Location(1, i) for i in range(N_ROBOTS)]
            self.robot_locs.sort()
            self.stack_locs = ([Location(1, i) for i in range(N_ROBOTS)] 
                               + [Location(2, i) for i in range(N_ROBOTS)])
            self.stack_locs.sort()
            return True
        else:
            print("Error: Cannot organize in rows.")
            return False
        
    def enum(self):
        """
        Enumerates the state by assigning a unique number to each state.
        
        First, enumerate the locations of the robots and multiply this value 
        by the number of possible locations of stacks and possible orders 
        values. Second, enumerate the locations of the stacks and multiply
        this value by the number of possible orders values. Last, enumerate 
        the number of possible orders values. Add all these together to get 
        the final enumeration of the state.
        
        
        Returns
        -------
        int
            The enumeration of the state.

        """
        map_idx_to_loc = lambda i: Location(math.floor(i / N_COLS), i % N_COLS)
        valid_locations = list(map(map_idx_to_loc, range(N_ROWS * N_COLS)))
                
        
        ## enumerate the location of robots
        enum_robots = 0
        locations = copy.deepcopy(valid_locations)
        for i in range(N_ROBOTS):
            idx = locations.index(self.robot_locs[i])
            if i == N_ROBOTS - 1:
                enum_robots += idx
            else:
                locations = locations[1:]
                for j in range(idx):
                    enum_robots += nCr(len(locations), N_ROBOTS - i - 1)
                    locations = locations[1:]
            
        possible_stacks_orders = (nCr(N_ROWS * N_COLS, N_STACKS)
                                  * (N_ITEMS+1)**N_STACKS)
        
        
        ## enumerate the locations of stacks
        enum_stacks = 0
        locations = copy.deepcopy(valid_locations)
        for i in range(N_STACKS):
            idx = locations.index(self.stack_locs[i])
            if i == N_STACKS - 1:
                enum_stacks += idx
            else:
                locations = locations[1:]
                for j in range(idx):
                    enum_stacks += nCr(len(locations), N_STACKS - i - 1)
                    locations = locations[1:]
            
        possible_orders = (N_ITEMS+1)**N_STACKS
            
        ## enumerate the order state variable
        enum_orders = 0
        for i in range(N_STACKS):
            enum_orders += self.orders[i] * (N_ITEMS+1)**(N_STACKS-1-i)
            
        enum = (enum_robots * possible_stacks_orders
               + enum_stacks * possible_orders
               + enum_orders)
        return enum
    
    def set_by_enum(self, num):
        # possible_stacks_orders = (nCr(N_ROWS * N_COLS, N_STACKS)
        #                           * (ITEMS_PER_STACK+1)**N_STACKS)
        
        # possible_orders = (ITEMS_PER_STACK+1)**N_STACKS
        
        # enum_robots = int(num / possible_stacks_orders)
        
        # cnt = 0
        # robot_locs = list(range(N_ROBOTS))
        # for i in range(N_ROBOTS):
            
        
        # enum_stacks = int(num / possible_orders) % possible_stacks_orders
        
        # enum_orders = num % possible_orders
        
        return 
    
    def grid(self):
        """
        Returns a visual representation of the state.

        Returns
        -------
        s : str
            Visual representation of the state.

        """
        s = ""
        for i in range(N_ROWS):
            s += "\n" + "-" * 6 * N_COLS + "---\n|"
            for j in range(N_COLS):
                loc = Location(i, j)
                cell = " "
                if loc in self.robot_locs:
                    cell += "R "
                else:
                    cell += "  "
                    
                if loc in self.stack_locs:
                    if self.orders[self.stack_locs.index(loc)] > 0:
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
        return s
    
    
    def __repr__(self):
        """
        Returns the string representation of a State object.

        Returns
        -------
        s : str
            The string representation of a State object.

        """
        s = self.grid()
        s += "robots = " + str(self.robot_locs) + '\n'
        s += "stacks = " + str(self.stack_locs) + '\n'
        s += "orders = " + str(self.orders) + '\n'
        return s