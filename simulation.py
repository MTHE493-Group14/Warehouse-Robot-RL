import random
import math
import copy

class Location:
    
    def __init__(self, r, c):
        self.row = r
        self.col = c
        return
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __repr__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"
    
    
    

class Warehouse:
    
    def __init__(self, rows, cols, robots, stacks, p):
        self.rows = rows # number of rows in the warehouse grid
        self.cols = cols # number of columns in the warehouse grid
        self.robots = robots # number of robots
        self.stacks = stacks # number of stacks
        self.order_prob = p # probability of an item being ordered at each time step
        self.picking = [Location(r, 0) for r in range(rows)] # the locations of picking stations
        return
    
    def __eq__(self, other):
        return self.rows == other.rows and self.cols == other.cols and self.robots == other.robots and self.stacks == other.stacks and self.picking == other.picking
    
    def __repr__(self):
        s = str(self.rows) + "x" + str(self.cols) + " grid"
        s += ", " + str(self.robots) + " robots"
        s += ", " + str(self.stacks) + " inventory stacks"
        s += ", " + str(self.order_prob * 100) + "% order probability"
        return s 
    
    
    
    
    
class State:
    
    def __init__(self, w):
        self.warehouse = w # the warehouse associated with the state
        
        # the locations of the robots
        rloc_idx = random.sample([x for x in range(w.rows * w.cols)], w.robots) # for each robot choose an integer representing the location
        self.robots_loc = [Location(math.floor(i/w.cols), i % w.cols) for i in rloc_idx] # convert integers to actual locations
        
        # the locations of the stacks
        sloc_idx = random.sample([x for x in range(w.rows * w.cols)], w.stacks) # for each stack choose an integer representing the location
        self.stacks_loc = [Location(math.floor(i/w.cols), i % w.cols) for i in sloc_idx] # convert integers to actual locations
            
        self.carry = [False]* w.robots # booleans indicating if the robot is carrying a stack
        self.ordered = [0]* w.stacks # the number of items ordered from each stack
        
        return
    
    def organize_in_rows(self):
        if self.warehouse.rows == 4 and self.warehouse.cols == 6 and self.warehouse.robots == 5 and self.warehouse.stacks == 10:
            self.robots_loc = [Location(1, i) for i in range(self.warehouse.robots)]
            self.stacks_loc = [Location(1, i) if i < self.warehouse.stacks / 2 else Location(2, i - self.warehouse.stacks / 2) for i in range(self.warehouse.stacks)]
        return
    
    def order_items(self):
        if random.random() < self.warehouse.order_prob:
            i = random.randint(1, self.warehouse.stacks) - 1
            self.ordered[i] = min(self.ordered[i] + 1, 9)
        return
    
    def __eq__(self, other):
        return self.warehouse == other.warehouse and self.robots_loc == other.robots_loc and self.stacks_loc == other.stacks_loc and self.carry == other.carry and self.ordered == other.ordered
    
    def __repr__(self):
        s = ""
        for i in range(self.warehouse.rows):
            s += "\n" + "-" * 6 * self.warehouse.cols + "---\n|"
            for j in range(self.warehouse.cols):
                loc = Location(i, j)
                a = " "
                if loc in self.robots_loc:
                    if self.carry[self.robots_loc.index(loc)]:
                        a += "R "
                    else:
                        a += "r "
                else:
                    a += "  "
                    
                if loc in self.stacks_loc:
                    if self.ordered[self.stacks_loc.index(loc)] > 0:
                        a += "$"
                    else:
                        a += "s"
                else:
                    a += " "
                    
                if loc in self.warehouse.picking:
                    s += "|" + a + " ||"
                else:
                    s += a + " |"
        s += "\n" + "-" * 6 * self.warehouse.cols + "---\n"
        # s += 'robots: ' + str(self.robots_loc)
        # s += '\nstacks: ' + str(self.stacks_loc)
        # s += '\ncarry: ' + str(self.carry)
        # s += '\nordered: ' + str(self.ordered) + "\n\n"
        return s
    
    



class Action:
    
    def __init__(self, a):
        self.dict = {"N": 0, "E": 1, "S": 2, "W": 3, "P": 4, "D": 5} # converts action names to action indices
        self.rev_dict = {0: "N", 1: "E", 2: "S", 3: "W", 4: "P", 5: "D"} # converts action indices to action names
        
        # if given the action name
        if type(a) == str and a in self.dict.keys(): # check if the name is valid
            self.name = a
            self.id = self.dict[a]
        # if given the action index
        elif type(a) == int and a in self.rev_dict.keys(): # check if the index is valid
            self.name = self.rev_dict[a]
            self.id = a
        else: # default: set action as "drop"
            self.name = "D"
            self.id = self.dict["D"]
        return
    
    def enumerate_class():
        pass

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id
    
    def __repr__(self):
        return self.name
    

    
    
    
    
    
class Actions:
    
    def __init__(self, w):
        
        self.warehouse = w # the warehouse associated with the actions
        self.actions = [Action(random.choice(["N", "E", "S", "W", "P", "D"])) for i in range(w.robots)] # list of actions
        return
    
    def enumerate_actions():
        pass
    
    def __repr__(self):
        return "( " +  " ".join([self.actions[i].name for i in range(self.warehouse.robots)]) + " )"
    
    def __eq__(self, other):
        return self.actions == other.actions
    
    
    
    
class Agent:
    
    def __init__(self, w, s):
        self.warehouse = w # the warehouse associated with the actions
        self.state = s # the current state of the agent
        self.t = 0 # the current time step
        self.cost = 0 # the current accumulative cost
        self.returned = 0 # the accumulative number of stacks returned
        return
    
    def calculate_state(self, a):
        """
        Determine which new state will be entered if taking this action in the current state 
        
        Determines new locations of robots
        Determines new locations of stacks
        Determines which robots are carrying items in the new state
        Determines which stacks still have ordered items
        Returns new state object 
        """
        current_state = self.state
        new_state = copy.deepcopy(current_state)

        for i in range(self.warehouse.robots):
            try:  # checks if there is the robot in the same location as a stack
                stack_num = current_state.stacks_loc.index(current_state.robots_loc[i])  # stores that stack number
            except ValueError:
                stack_num = -1

            if a.actions[i].name == "N":  # If the robot has chosen to move north
                new_state.robots_loc[i].row -= 1
                if stack_num != -1 and current_state.carry[i]:
                    new_state.stacks_loc[stack_num].row -= 1
            elif a.actions[i].name == "E":  # If the robot has chosen to move east
                new_state.robots_loc[i].col += 1
                if stack_num != -1 and current_state.carry[i]:
                    new_state.stacks_loc[stack_num].col += 1
            elif a.actions[i].name == "S":  # If the robot has chosen to move south
                new_state.robots_loc[i].row += 1
                if stack_num != -1 and current_state.carry[i]:
                    new_state.stacks_loc[stack_num].row += 1
            elif a.actions[i].name == "W":  # If the robot has chosen to move west
                new_state.robots_loc[i].col -= 1
                if stack_num != -1 and current_state.carry[i]:
                    new_state.stacks_loc[stack_num].col -= 1
            elif a.actions[i].name == "D":  # If the robot has chosen to drop off a stack
                new_state.carry[i] = False
            elif a.actions[i].name == "P":
                if stack_num != -1:  # If the robot has chosen to pick up a stack
                    new_state.carry[i] = True
            else:
                print("Error: Invalid State Name entry")  # An invalid state was passed to this function
        
        for j in range(self.warehouse.stacks):
            if new_state.stacks_loc[j] == current_state.stacks_loc[j] and new_state.stacks_loc[j] in self.warehouse.picking:
                new_state.ordered[j] = max(new_state.ordered[j] - 1, 0)

        # new_state = self.state
        return new_state
    
    def possible_state(self, new_state):
        """
        Checks if transitioning from the agent's current state to a new state is possible 
        
        Check if robots are outside the grid in state2 
        Check if 2 robots are in the same location in state2 
        Check if 2 stacks are in the same location in state2 
        Check if 2 robots moved through one another (I.e. switched locations transitioning from the current state to state2)
        Return a boolean value if its available 
        """
        n = new_state.warehouse.rows
        m = new_state.warehouse.cols
        
        r_taken_loc = []
        for r in new_state.robots_loc:
            if r.col < 0 or r.col >= m or r.row < 0 or r.row >= n:
                return False
            if r in r_taken_loc:
                return False
            else: 
                r_taken_loc.append(r)
                
        s_taken_loc = []
        for s in new_state.stacks_loc:
            if s.col < 0 or s.col >= m or s.row < 0 or s.row >= n:
                return False
            if s in s_taken_loc:
                return False 
            else: 
                s_taken_loc.append(s)
        
        robot_pos1 = self.state.robots_loc
        robot_pos2 = new_state.robots_loc
        for i in range(self.warehouse.robots):
            for j in range(self.warehouse.robots):
                if robot_pos2[i] == robot_pos1[j] and robot_pos1[i] == robot_pos2[j] and i != j:
                    return False
        return True
    
    def policy(self):
        """
        Since we are not implementing the q-learning alg yet, just pick a random action 
        
        Pick a random action, calculate new state, check if the state transition is possible 
        If the state transition is not possible, pick a new random action and try again 
        Return the action 
        """
        possibleState = False
        while not possibleState: # run this function until possible state is true, this tells us that its possible to go to next state
            a = Actions(self.warehouse) # create random list of actions
            new_state = self.calculate_state(a) # calculate new state
            possibleState = self.possible_state(new_state) # see if new state is possible
        return a # if possible then return list of actions.
    
    def baseline_policy(self):
        """
        A policy that we will compare its performance to the learned policy
        """
        a = Actions(self.warehouse)
        normal = True
        
        for r_idx in range(self.warehouse.robots):
            if self.state.robots_loc[r_idx].row == 0 or self.state.robots_loc[r_idx].row == 3:
                normal = False
                a.actions = [Action("D") for i in range(self.warehouse.robots)]
                if self.state.robots_loc[r_idx].col > 0:
                    a.actions[r_idx] = Action("W")
                elif self.state.robots_loc[r_idx].row == 0:
                    a.actions[r_idx] = Action("S")
                elif self.state.robots_loc[r_idx].row == 3:
                    a.actions[r_idx] = Action("N")
                    
        if normal:
            m = max(self.state.ordered)
            s_idx = self.state.ordered.index(m)
            if m > 0 and self.state.stacks_loc[s_idx].col > 0 and (not any(self.state.carry) or all(self.state.carry)):
                r_cols = [self.state.robots_loc[i].col for i in range(self.warehouse.robots)]
                r_idx = r_cols.index(self.state.stacks_loc[s_idx].col)
                if self.state.stacks_loc[s_idx].row == 1 and self.state.robots_loc[r_idx].row == 1:
                    if self.state.carry[r_idx]:
                        for i in range(self.warehouse.robots):
                            if i == r_idx:
                                a.actions[i] = Action("N")
                            elif self.state.robots_loc[i].col < self.state.robots_loc[r_idx].col:
                                a.actions[i] = Action("E")
                            else:
                                a.actions[i] = Action("D")
                    else:
                        a.actions = [Action("P") for i in range(self.warehouse.robots)]
                elif self.state.stacks_loc[s_idx].row == 2 and self.state.robots_loc[r_idx].row == 2:
                    if self.state.carry[r_idx]:
                        for i in range(self.warehouse.robots):
                            if i == r_idx:
                                a.actions[i] = Action("S")
                            elif self.state.robots_loc[i].col < self.state.robots_loc[r_idx].col:
                                a.actions[i] = Action("E")
                            else:
                                a.actions[i] = Action("D")
                    else:
                        a.actions = [Action("P") for i in range(self.warehouse.robots)]
                elif self.state.stacks_loc[s_idx].row == 1 and self.state.robots_loc[r_idx].row == 2 and not self.state.carry[r_idx]:
                    a.actions = [Action("N") for i in range(self.warehouse.robots)]
                elif self.state.stacks_loc[s_idx].row == 2 and self.state.robots_loc[r_idx].row == 1 and not self.state.carry[r_idx]:
                    a.actions = [Action("S") for i in range(self.warehouse.robots)]
                else:
                    a.actions = [Action("D") for i in range(self.warehouse.robots)]
            else:
                a.actions = [Action("D") for i in range(self.warehouse.robots)]
        return a
    
    def update_cost(self):
        self.cost += sum(self.state.ordered)
        return
    
    def __repr__(self):
        return str(self.state) + "t = " + str(self.t) + ", cost = " + str(self.cost) + ", returned = " + str(self.returned)
        
        

def main():
    w = Warehouse(rows=4, cols=6, robots=5, stacks=10, p=0.2)
    print(w)
    
    x0 = State(w)
    agent = Agent(w, x0)
    
    
    while(agent.t < 10):
        agent.state.order_items()
        print(agent)
        a = agent.policy()
        num_ordered = sum(agent.state.ordered)
        agent.state = agent.calculate_state(a)
        agent.returned += num_ordered - sum(agent.state.ordered)
        agent.update_cost()
        agent.t += 1
    return

def main2():
    w = Warehouse(rows=4, cols=6, robots=5, stacks=10, p=0.5)
    print(w)
    
    x0 = State(w)
    x0.organize_in_rows()
    agent = Agent(w, x0)
    
    
    while(agent.t < 40):
        agent.state.order_items()
        print(agent)
        a = agent.baseline_policy()
        num_ordered = sum(agent.state.ordered)
        agent.state = agent.calculate_state(a)
        agent.returned += num_ordered - sum(agent.state.ordered)
        agent.update_cost()
        agent.t += 1
    return

main2()







