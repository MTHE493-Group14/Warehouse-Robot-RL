from environment import Environment


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


def train(n_reps=10000, n_iter=20, overwrite=False):
    env = Environment()
    if not overwrite:
        env.agent.q.read_qtable()
        
    for rep in range(n_reps):
        env.state.reset()
        for time_step in range(n_iter):
            a = env.agent.epsilon_greedy_policy(env.state, 0.9)
            previous_state = env.state
            env.state = env.calculate_state(env.state, a)
            env.update_cost()
            env.agent.tables.update(previous_state, env.state, a, sum(env.state.orders))
    env.agent.q.save_qtable()
    return

def evaluate(n_reps=100, n_iter=100, show=29, train=False):
    env = Environment()
    env.agent.q.read_qtable()
    
    for time_step in range(show):
        print('\n')
        print("t = " + str(time_step))
        print(env)
        a = env.agent.greedy_policy(env.state)
        print("actions = " + str(a.actions))
        print('state = ' + str(env.state.enum()) + ', action = ' + str(a.enum()))
        env.state = env.calculate_state(env.state, a)
        env.update_cost()
    
    for rep in range(n_reps):
        env.state.reset()
        for time_step in range(n_iter):
            a = env.agent.greedy_policy(env.state)
            if train:
                previous_state = env.state
            env.state = env.calculate_state(env.state, a)
            env.update_cost()
            if train:
                env.agent.tables.update(previous_state, env.state, a, sum(env.state.orders))
    env.agent.q.save_qtable()
    print('\nscore = ' + str(env.cost/n_iter/n_reps))
    return

def baseline(n_iter=1000, show=10):
    env = Environment()
    if not env.state.baseline_organization():
        return
    
    for time_step in range(show):
        print('\n')
        print("t = " + str(time_step))
        print(env)
        a = env.agent.baseline_policy(env.state)
        print("actions = " + str(a.actions))
        print('state = ' + str(env.state.enum()) + ', action = ' + str(a.enum()))
        env.state = env.calculate_state(env.state, a)
        env.update_cost()
        
    for time_step in range(n_iter):
        a = env.agent.greedy_policy(env.state)
        env.state = env.calculate_state(env.state, a)
        env.update_cost()
    
    print('\nscore = ' + str(env.cost/n_iter))
    return

# train(n_reps=100, n_iter=100, overwrite=True)

for i in range(1000):
    print('\n', i)
    train()
    evaluate(train=True)
    
# baseline()
