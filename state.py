import random
import copy
import numpy as np

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
        
        robot_locs = [(0,1), (1,2), (1,1)]
        stack_locs = [(0,1), (1,1), (0,0)]
        orders = [0, 1, 1]
        
    The robot_locs list would be reordered by switching the order of the last 
    two locations. The stack_locs list would be reordered by moving the last 
    location to the front of the list. Since the orders list contains numbers 
    that correspond to particular stacks, the orders list should be reordered
    by performing the same rearrangements that the stack_locs list made 
    instead of reordering the list based on the integers it contains. 
    
    Our resulting state would be as follows:
        
        robot_locs = [(0,1), (1,1), (1,2)]
        stack_locs = [(0,0), (0,1), (1,1)]
        orders = [1, 0, 1]
    
    Attributes
    ----------
    valid_locs : [Location]
        The valid locations that a robot or stack could be located in. This
        attribute should not be changed.
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
        self.valid_locs = list(map(Location.idx_to_loc, range(-1, N_ROWS * N_COLS)))
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
        self.robot_locs = random.sample(self.valid_locs, k=N_ROBOTS)
        self.robot_locs.sort()
        self.stack_locs = random.sample(self.valid_locs, k=N_STACKS)
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
        
        ### NO LONGER WORKS WITH NEW WAREHOUSE SHAPE
        
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
        # enumerate the location of robots
        enum_robots = 0
        locations = copy.deepcopy(self.valid_locs)
        for i in range(N_ROBOTS):
            idx = locations.index(self.robot_locs[i])
            if i == N_ROBOTS - 1:
                enum_robots += idx
            else:
                locations = locations[1:]
                for _ in range(idx):
                    enum_robots += nCr(len(locations), N_ROBOTS - i - 1)
                    locations = locations[1:]
            
        possible_stacks_orders = (nCr(N_ROWS * N_COLS + 1, N_STACKS)
                                  * (N_ITEMS+1)**N_STACKS)
        
        
        # enumerate the locations of stacks
        enum_stacks = 0
        locations = copy.deepcopy(self.valid_locs)
        for i in range(N_STACKS):
            idx = locations.index(self.stack_locs[i])
            if i == N_STACKS - 1:
                enum_stacks += idx
            else:
                locations = locations[1:]
                for _ in range(idx):
                    enum_stacks += nCr(len(locations), N_STACKS - i - 1)
                    locations = locations[1:]
            
        possible_orders = (N_ITEMS+1)**N_STACKS
            
        # enumerate the order state variable
        enum_orders = 0
        for i in range(N_STACKS):
            enum_orders += self.orders[i] * (N_ITEMS+1)**(N_STACKS-1-i)
            
        enum = (enum_robots * possible_stacks_orders
               + enum_stacks * possible_orders
               + enum_orders)
        return enum
    
    def features(self):
        """
        Return the features values for a state.

        Returns
        -------
        f : [int]
            The list of feature values.

        """
        # a1 = [Location(0, -1), Location(0, 0), Location(0, 1), Location(1, 0)]
        # a2 = [Location(0, 1), Location(0, 2), Location(1, 0), Location(1, 1)]
        # a3 =  [Location(0, 2), Location(0, 3), Location(1, 1), Location(1, 2), Location(1, 3)]

        a1 = [Location(0, -1), Location(0, 0)]
        a2 = [Location(0, 0), Location(0, 1), Location(1, 0)]
        a3 =  [Location(0, 1), Location(0, 2), Location(1, 0), Location(1, 1)]
        a4 =  [Location(0, 2), Location(0, 3), Location(1, 1), Location(1, 2)]
        a5 =  [Location(0, 3), Location(1, 2), Location(1, 3)]
        a6 =  [Location(1, 3)]
        n_areas = 6

        nr = np.sum((np.isin(self.robot_locs, a1), 
                     np.isin(self.robot_locs, a2), 
                     np.isin(self.robot_locs, a3), 
                     np.isin(self.robot_locs, a4), 
                     np.isin(self.robot_locs, a5), 
                     np.isin(self.robot_locs, a6)), axis=1)
        fr = np.zeros((n_areas, N_ROBOTS+1), dtype=int)
        fr[np.arange(n_areas), nr] = 1

        ns = np.sum((np.isin(self.stack_locs, a1), 
                     np.isin(self.stack_locs, a2), 
                     np.isin(self.stack_locs, a3), 
                     np.isin(self.stack_locs, a4), 
                     np.isin(self.stack_locs, a5), 
                     np.isin(self.stack_locs, a6)), axis=1)
        fs = np.zeros((n_areas, N_STACKS+1), dtype=int)
        fs[np.arange(n_areas), ns] = 1

        no = np.sum((np.isin(self.stack_locs, a1), 
                     np.isin(self.stack_locs, a2), 
                     np.isin(self.stack_locs, a3), 
                     np.isin(self.stack_locs, a4), 
                     np.isin(self.stack_locs, a5), 
                     np.isin(self.stack_locs, a6)) * np.asarray(self.orders), axis=1)
        fo = np.zeros((n_areas, N_STACKS+1), dtype=int)
        fo[np.arange(n_areas), no] = 1

        f = np.multiply(np.multiply(fr[:, np.newaxis].reshape(n_areas, -1, 1), fs[:, np.newaxis]).reshape(n_areas, -1, 1), fo[:, np.newaxis]).flatten()
        return f

    def features2(self):
        """
        Return the features values for a state.

        Returns
        -------
        f : [int]
            The list of feature values.
        """
        rows = [loc.row for loc in self.robot_locs] + [loc.row for loc in self.stack_locs]
        cols = [loc.col for loc in self.robot_locs] + [loc.col for loc in self.stack_locs]

        fr = np.zeros((N_ROBOTS + N_STACKS, N_ROWS), dtype=int)
        fr[np.arange(N_ROBOTS + N_STACKS), rows] = 1

        fs = np.zeros((N_ROBOTS + N_STACKS, N_COLS + 1), dtype=int)
        fs[np.arange(N_ROBOTS + N_STACKS), cols] = 1

        f = np.concatenate((fr.flatten(), fs.flatten(), self.orders), axis=None)
        return f
    
    def value_estimate(self):
        """
        Return a q-value estimate.
        
        Used for initializing q-tables and function approximator weights.

        Returns
        -------
        q : float
            The estimated q-value for that state.

        """
        q = 0
        for s in self.stack_locs:
            q += s.row + s.col + 1
        q *= N_STACKS / N_ROBOTS
        return q
    
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
            s += "\n" + "-" * (6 * (N_COLS + 1) - 2) + "---\n|"
            if i == 0:
                for j in range(-1, N_COLS):
                    loc = Location(i, j)
                    if loc in self.robot_locs:
                        s += " R "
                    else:
                        s += "   "
                        
                    if loc in self.stack_locs:
                        if self.orders[self.stack_locs.index(loc)] > 0:
                            s += "$ |"
                        else:
                            s += "s |"
                    else:
                        s += "  |"
            else:
                s += '/////|'
                for j in range(N_COLS):
                    loc = Location(i, j)
                    if loc in self.robot_locs:
                        s += " R "
                    else:
                        s += "   "
                        
                    if loc in self.stack_locs:
                        if self.orders[self.stack_locs.index(loc)] > 0:
                            s += "$ |"
                        else:
                            s += "s |"
                    else:
                        s += "  |"
        s += "\n" + "-" * (6 * (N_COLS + 1) - 2) + "---\n"
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