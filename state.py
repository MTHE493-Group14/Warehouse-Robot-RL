import random
import math
import copy

from location import Location
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, ITEMS_PER_STACK
from util import nPr

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
        A list of boolean values indicating which of the robots are lifting 
        stacks. The length of lift is equal to N_ROBOTS.
    orders : [int]
        The number of ordered items that each stack contains. Each value in 
        orders cannot be any larger than ITEMS_PER_STACK. The length of orders 
        is equal to N_STACKS.
    
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
        map_idx_to_loc = lambda i: Location(math.floor(i / N_COLS), i % N_COLS)
        valid_locations = list(map(map_idx_to_loc, range(N_ROWS * N_COLS)))
        self.robot_locs = random.sample(valid_locations, k=N_ROBOTS)
        self.stack_locs = random.sample(valid_locations, k=N_STACKS)
        self.lift = [False]* N_ROBOTS
        self.orders = [0]* N_STACKS
        return
    
    
    def baseline_organization(self):
        """
        Initializes robot and stack locations for the baseline policy.
        
        The baseline policy requires that the stacks are located in the middle
        2 rows of the warehouse grid and the robots are located in one of 
        those 2 middle rows in the grid. This method must be called before 
        using the baseline policy.
        
        The method assumes that the warehouse has 4 rows, at least as many 
        columns as robots, and twice as many stacks as robots.

        Returns
        -------
        None.

        """
        ### RAISE EXCEPTION
        if (N_ROWS >= 4 and N_COLS >= N_ROBOTS and N_STACKS == 2*N_ROBOTS):
            self.robot_locs = [Location(1, i) for i in range(N_ROBOTS)]
            self.stack_locs = ([Location(1, i) for i in range(N_ROBOTS)] 
                               + [Location(2, i) for i in range(N_ROBOTS)])
            return True
        else:
            print("Error: Cannot organize in rows.")
            return False
        
    def enum(self):
        """
        Enumerates the state.
        
        This method will be useful when for the Q-table when Q-learning is 
        implemented.
        
        First, enumerate the locations of the robots and multiply this value 
        by the number of possible locations of stacks, lift boolean values, 
        and orders. Second, enumerate the locations of the stacks and multiply
        this value by the number of possible lift boolean values and orders.
        Next, enumerate the lift boolean values and multiply this value by the
        number of possible orders. Last, enumerate the number of possible 
        orders. Add all these together to get the final enumeration of the 
        state.
        
        
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
            locations = locations[:idx] + locations[idx+1:]
            coeff = nPr(len(locations), N_ROBOTS-1-i)
            enum_robots += idx * coeff
            
        possible_stacks_lift_orders = (nPr(N_ROWS * N_COLS, N_STACKS)
                                       * 2**N_ROBOTS
                                       * (ITEMS_PER_STACK+1)**N_STACKS)
        
        
        ## enumerate the locations of stacks
        enum_stacks = 0
        locations = copy.deepcopy(valid_locations)
        for i in range(N_STACKS):
            idx = locations.index(self.stack_locs[i])
            locations = locations[:idx] + locations[idx+1:]
            coeff = nPr(len(locations), N_STACKS-1-i)
            enum_stacks += idx * coeff
            
        possible_lift_orders = (2**N_ROBOTS
                                * (ITEMS_PER_STACK+1)**N_STACKS)
            
        
        ## enumerate the lift state variable
        enum_lift = 0
        for i in range(N_ROBOTS):
            enum_lift += self.lift[i] * 2 ** (N_ROBOTS - 1 - i)
        possible_orders = (ITEMS_PER_STACK+1)**N_STACKS
            
        ## enumerate the order state variable
        enum_orders = 0
        for i in range(N_STACKS):
            enum_orders += self.orders[i] * (ITEMS_PER_STACK+1)**(N_STACKS-1-i)
            
        enum = (enum_robots * possible_stacks_lift_orders
               + enum_stacks * possible_lift_orders
               + enum_lift * possible_orders
               + enum_orders)
        return enum
    
    def set_by_enum(self, num):
        # map_idx_to_loc = lambda i: Location(math.floor(i / N_COLS), i % N_COLS)
        # valid_locations = list(map(map_idx_to_loc, range(N_ROWS * N_COLS)))
        
        # possible_stacks_lift_orders = (nPr(N_ROWS * N_COLS, N_STACKS)
        #                                * 2**N_ROBOTS
        #                                * (ITEMS_PER_STACK+1)**N_STACKS)
        
        # ## enumerate the location of robots
        # enum_robots = 0
        # locations = copy.deepcopy(valid_locations)
        # for i in range(N_ROBOTS):
        #     idx = locations.index(self.robot_locs[i])
        #     locations = locations[:idx] + locations[idx+1:]
        #     coeff = nPr(len(locations), N_ROBOTS-1-i)
        #     enum_robots += idx * coeff
            
        # locations = copy.deepcopy(valid_locations)
        # for i in range(N_ROBOTS):
            
        #     robot_idx = int(num / num_acts**(N_ROBOTS - 1 - i)) % num_acts
        #     robot_loc = locations[robot_idx]
            
            
        
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
                    if self.lift[self.robot_locs.index(loc)]:
                        cell += "R "
                    else:
                        cell += "r "
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
        s += "lifting = " + str(self.lift) + '\n'
        s += "ordered = " + str(self.orders) + '\n'
        return s