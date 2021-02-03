import random

from warehouse_parameters import POLICY_TYPE, N_STACKS, ORDER_PROB, ITEMS_PER_STACK
from state import State
from agent import Agent


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
        there is already ITEMS_PER_STACK ordered items on the stack.

        Returns
        -------
        None.

        """
        for i in range(N_STACKS):
            if random.random() < ORDER_PROB:
                if self.state.orders[i] < ITEMS_PER_STACK:
                    self.state.orders[i] += 1
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
        return (str(self.state)
                + "cost = " + str(self.cost) 
                + ", total_orders = " + str(self.total_orders) 
                + ", total_returns = " + str(self.total_returns))