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
    """
    
    def __init__(self):
        self.state = State()
        self.agent = Agent()
        self.cost = 0
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
        return str(self.state) + "cost = " + str(self.cost)