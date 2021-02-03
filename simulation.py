import numpy as np

from environment import Environment
from warehouse_parameters import N_ITER


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

Each inventory stack will contain a fixed number of items. At the beginning of 
each time step, each item has a small chance of being ordered by an Amazon 
customer.

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


def main():
    env = Environment()
    
    for time_step in range(N_ITER):
        print("\n\nt = " + str(time_step))
        env.order_items()
        print(env)
        # print(env.state.grid())
        a = env.agent.policy(env.state)
        print("actions = " + str(a.actions))
        # print(env.state.enum(), a.enum())
    
        s1 = env.state
        env.state = env.agent.calculate_state(env.state, a)
        env.total_returns += sum(s1.orders) - sum(env.state.orders)
        env.update_cost()
        env.agent.q.update(s1, env.state, a, sum(env.state.orders))
    print(env.agent.q)
    return

def test():
    from state import State
    from location import Location
    
    x = State()

    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,0)
    x.lift[0] = False
    x.orders[0] = 0
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,0)
    x.lift[0] = False
    x.orders[0] = 1
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,0)
    x.lift[0] = True
    x.orders[0] = 0
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,0)
    x.lift[0] = True
    x.orders[0] = 1
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,1)
    x.lift[0] = False
    x.orders[0] = 0
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(0,1)
    x.lift[0] = False
    x.orders[0] = 1
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(1,0)
    x.lift[0] = False
    x.orders[0] = 0
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(1,0)
    x.lift[0] = False
    x.orders[0] = 1
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(1,1)
    x.lift[0] = False
    x.orders[0] = 0
    print(x.grid())
    print(x.enum())
    
    x.robot_locs[0] = Location(0,0)
    x.stack_locs[0] = Location(1,1)
    x.lift[0] = False
    x.orders[0] = 1
    print(x.grid())
    print(x.enum())
    
    return
    

main()
