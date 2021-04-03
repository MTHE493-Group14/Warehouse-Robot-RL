from environment import Environment
import time
import numpy as np


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


def train(method, train_reps=1000, train_iters=1000, eval_reps=100, eval_iters=100, overwrite=False):
    env = Environment(method, overwrite)
    greedy_actions = env.agent.tables.greedy_actions()
    if overwrite:
        avg_cost, max_avg_cost, min_avg_cost = evaluate(method, eval_reps, eval_iters)
        env.agent.performance.update(0, avg_cost, max_avg_cost, min_avg_cost)
        
    for _ in range(train_reps):
        env.state.reset()
        for _ in range(train_iters):
            a = env.agent.epsilon_random_greedy_policy(env.state, 0.95)
            # a = env.agent.epsilon_random_greedy_policy(env.state, 0.95)
            previous_state = env.state
            env.state = env.calculate_state(env.state, a)
            env.update_cost()
            if method == 'tabular':
                env.agent.tables.update(previous_state, env.state, a, sum(env.state.orders))
            else:
                env.agent.lfa.update(previous_state, env.state, a, sum(env.state.orders))

    if method == 'tabular':
        env.agent.tables.save(env.filename)
    else:
        env.agent.lfa.save(env.filename)

    avg_cost, max_avg_cost, min_avg_cost = evaluate(method, eval_reps, eval_iters)
    env.agent.performance.update(train_reps*train_iters, avg_cost, max_avg_cost, min_avg_cost)
    env.agent.performance.save(method, env.filename)
    # env.agent.performance.plot()
    return np.all(greedy_actions == env.agent.tables.greedy_actions())




def evaluate(method, n_reps=100, n_iter=100, show=100):
    env = Environment(method, overwrite=False)
    
    for time_step in range(show):
        a = env.agent.greedy_policy(env.state)
        print('\n')
        print("t = " + str(time_step))
        print(env.state.grid())
        print("actions = " + str(a.actions))
        # print('state = ' + str(env.state.enum()) + ', action = ' + str(a.enum()))
        env.state = env.calculate_state(env.state, a)
        env.update_cost()
    
    env.cost = 0
    max_cost = 0
    min_cost = -1
    for _ in range(n_reps):
        env.state.reset()
        start_cost = env.cost
        for _ in range(n_iter):
            a = env.agent.greedy_policy(env.state)
            env.state = env.calculate_state(env.state, a)
            env.update_cost()
        rep_cost = env.cost - start_cost
        max_cost = max(max_cost, rep_cost)
        if rep_cost < min_cost or min_cost == -1:
            min_cost = rep_cost

    avg_cost = env.cost/n_iter/n_reps
    max_avg_cost = max_cost / n_iter
    min_avg_cost = min_cost / n_iter
    print(  '\navg_cost = ' + str(avg_cost) + 
            ', max_avg_cost = ' + str(max_avg_cost) + 
            ', min_avg_cost = ' + str(min_avg_cost))
    return avg_cost, max_avg_cost, min_avg_cost






# def baseline(n_iter=1000, show=10):
#     env = Environment()
#     if not env.state.baseline_organization():
#         return
    
#     for time_step in range(show):
#         print('\n')
#         print("t = " + str(time_step))
#         print(env)
#         a = env.agent.baseline_policy(env.state)
#         print("actions = " + str(a.actions))
#         print('state = ' + str(env.state.enum()) + ', action = ' + str(a.enum()))
#         env.state = env.calculate_state(env.state, a)
#         env.update_cost()
        
#     for time_step in range(n_iter):
#         a = env.agent.greedy_policy(env.state)
#         env.state = env.calculate_state(env.state, a)
#         env.update_cost()
    
#     print('\nscore = ' + str(env.cost/n_iter))
#     return


# train('fa', train_reps=1000, train_iters=100, eval_reps=100, eval_iters=100, overwrite=True)
for i in range(1000):
    print('\n', i)
    converged = train('tabular', train_reps=1000, train_iters=100, eval_reps=100, eval_iters=100, overwrite=False)
    if converged:
        print("LFGGG\n\n\n")
        break

# evaluate(train=True)
    
# baseline()
