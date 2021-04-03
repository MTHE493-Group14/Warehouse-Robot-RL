def new_baseline_policy(self, current_state):
    """
    Determines what action to take in the current state if following the
    baseline_policy.
    
    In order to evaluate the policy learned by the reinforcement learning
    algorithm, we must compare its performance to the performance of 
    another policy. This baseline policy keeps all the stacks and robots 
    in the 2 middle rows until a stack needs to be returned to a picking 
    station.
    
    An example of what the warehouse looks like is:
    -------------------------------
    |  P  |     |     |     |     |
    -------------------------------
    |/////| R s | R s |  s  |  s  |
    -------------------------------
    
    For each column in the grid, there is 1 stack and 2 robots for the 
    entire warehouse. The stack with the highest number of outstanding 
    ordered items that is not already at a picking station is identified. 
    All robots will be in the bottom row where all stacks are located, 
    then the robot in the same column as the desired stack will move the
    stack into the top row. The same robot will then move the desired 
    stack to the leftmost column in the grid (where the picking stations 
    are), and lastly the robot will return the desired stack to the bottom
    row while the other robot shifts the stacks to the right to 
    make room for the desired stack.

    When following this policy, there are 5 types of states. Each type of 
    state has a unique list of actions that should be taken when in that 
    type of state. The 5 cases are as follows:
    
    Case 1:
        All stacks and robots are in the bottom row. Any stack 
        that has had items ordered are at the picking station or
        delivering items.
        
        At this state, no action needs to be taken and each robot can 
        do nothing.
    Case 2:
        All stacks and robots are in the bottom row but the two robots are
        not in the same column as the stacks with the most ordered items 
        that is not already at a picking station. 
        
        In this type of state, the robots need to move to the column with the 
        desired stack. A robot should move left or right to the correct column.
    Case 3:
        All stacks and robots are in the bottom row and the robots are in the
        same columns as the stacks with the most ordered items that is not
        already at a picking station. 
        
        In this type of state, the robots are ready to start moving the 
        desired stack to the picking station. The robot in the same column
        as the desired stack should move the stack up to the top row. The 
        other robot does nothing.
    Case 4: 
        The three stacks and other robot are in the bottom row, one robot
        and stack are in the top row. This robot and stack move left 
        to the picking station so the item can be collected by a worker but
        it has not yet reached the leftmost column in the warehouse grid. The other 
        robot is staying at the bottom row.
        
        In this type of state, the robot in the top row can continue moving 
        left with the desired stack to a picking station. The other robot
        will have no action and stay in the bottom row.
    Case 5:
        The three stacks and other robot are in the bottom row, one robot
        and stack are in the top row at the picking station. The other 
        robot is staying at the bottom row.
      
        In this type of state, the stacks in the bottom row can shift
        over with the stacks in their column to make room for the desired 
        stack to return to the bottom row at the leftmost column. 
        
        While the desired stack stays at the picking station for
        a few time steps so the worker can collect the ordered item, the other 
        robot will move stacks to the left of the original column of the 
        selected stack to the right. Any columns to the right of the original 
        column will stay at their current position.

    Returns
    -------
    a : Actions
        The list of actions that should be taken in the current state if 
        following the baseline policy.
"""