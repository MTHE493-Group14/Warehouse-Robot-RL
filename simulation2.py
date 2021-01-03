import random
import math
import copy

class Location:
    
    def __init__(self, x, y):
        self.row = x
        self.col = y
        return
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __repr__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"
    
    
class Warehouse:
    def __init__(self, n, m, i, j, p):
        self.rows = n
        self.cols = m
        self.robots = i
        self.stacks = j
        self.order_prob = p
        self.picking = []
        for i in range(n):
            self.picking.append(Location(i, 0))
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
        
        self.warehouse = w
        
        rloc_idx = random.sample([x for x in range(w.rows * w.cols)], w.robots)
        self.robots_loc = []
        for i in rloc_idx:
            self.robots_loc.append(Location(math.floor(i/w.cols), i % w.cols))
        
        sloc_idx = random.sample([x for x in range(w.rows * w.cols)], w.stacks)
        self.stacks_loc = []
        for i in sloc_idx:
            self.stacks_loc.append(Location(math.floor(i/w.cols), i % w.cols))
            
        self.carry = [False]* w.robots
        
        self.ordered = [False]* w.stacks
        
        return
    
    def order_items(self):
        if random.random() < self.warehouse.order_prob:
            self.ordered[random.randint(1, self.warehouse.stacks) - 1] = True
        return
    
    def __eq__(self, other):
        return self.warehouse == other.warehouse and self.robots_loc == other.robots_loc and self.stacks_loc == other.stacks_loc and self.carry == other.carry and self.ordered == other.ordered
    
    def __repr__(self):
        s = ""
        for i in range(self.warehouse.rows):
            s += "\n---------------------------------------------------------------\n|"
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
                    if self.ordered[self.stacks_loc.index(loc)]:
                        a += "$"
                    else:
                        a += "s"
                else:
                    a += " "
                    
                if loc in self.warehouse.picking:
                    s += "|" + a + " ||"
                else:
                    s += a + " |"
        s += "\n---------------------------------------------------------------\n"
        return s


class Action:
    
    def __init__(self, a):
        self.dict = {"N": 0, "E": 1, "S": 2, "W": 3, "P": 4, "D": 5}
        self.rev_dict = {0: "N", 1: "E", 2: "S", 3: "W", 4: "P", 5: "D"}
        
        if type(a) == int and a in self.rev_dict.keys():
            self.name = self.rev_dict[a]
            self.id = a
        elif type(a) == str and a in self.dict.keys():
            self.name = a
            self.id = self.dict[a]
        else:
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
        
        self.warehouse = w
        
        self.actions = []
        self.names = ""
        self.ids = []
        
        for i in range(w.robots):
            a = Action(random.choice(["N", "E", "S", "W", "P", "D"]))
            self.actions.append(a)
            self.names += a.name
            self.ids.append(a.id)
        return
    
    def enumerate_actions():
        pass
    
    def __repr__(self):
        return "( " +  " ".join(self.names) + " )"
    
    def __eq__(self, other):
        return self.names == other.names and self.ids == other.ids
    
     
class Agent:
    
    def __init__(self, w, s):
        
        self.warehouse = w
        self.state = s
        self.t = 0
        self.cost = 0
        
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
        print('cs', current_state)
        print('a',a)
        new_state = copy.deepcopy(current_state)

        for i in range(0, self.warehouse.robots):
            try:  # checks if there is the robot is at a stack
                stack_num = current_state.stacks_loc.index(current_state.robots_loc[i])  # stores that stack number
                stack_robot_pair = True if current_state.carry[i] and current_state.ordered[stack_num] else False
            except ValueError:
                stack_num = -1
                stack_robot_pair = False

            if a.actions[i].name == "N":  # If the robot has chosen to move north
                if stack_num != -1 and stack_robot_pair:
                    new_state.stacks_loc[stack_num].row += 1
                new_state.robots_loc[i].row += 1
            elif a.actions[i].name == "E":  # If the robot has chosen to move east
                if stack_num != -1 and stack_robot_pair:
                    new_state.stacks_loc[stack_num].col += 1
                new_state.robots_loc[i].col += 1
            elif a.actions[i].name == "S":  # If the robot has chosen to move south
                if stack_num != -1 and stack_robot_pair:
                    new_state.stacks_loc[stack_num].row -= 1
                new_state.robots_loc[i].row -= 1
            elif a.actions[i].name == "W":  # If the robot has chosen to move west
                if stack_num != -1 and stack_robot_pair:
                    new_state.stacks_loc[stack_num].col -= 1
                new_state.robots_loc[i].col -= 1
            elif a.actions[i].name == "D":  # If the robot has chosen to drop off a stack
                new_state.carry[i] = False
                if current_state.robots_loc[i].col == 0:  # If the robot drops the stack in the picking station
                    new_state.ordered[stack_num] = False
            elif a.actions[i].name == "P":  # If the robot has chosen to pick up a stack
                if stack_num != -1 and not stack_robot_pair:
                    if current_state.ordered[stack_num]:
                        new_state.carry[i] = True
            else:
                print("Error: Invalid State Name entry")  # An invalid state was passed to this function

        return new_state

    def possible_state(self, s2):
        """
        Checks if transitioning from the agent's current state to a new state is possible 
        Check if robots are outside the grid in state2 
        Check if 2 robots are in the same location in state2 
        Check if 2 stacks are in the same location in state2 
        Check if 2 robots moved through one another (I.e. switched locations transitioning from the current state to state2)
        Return a boolean value if its available 
        """
        
        r_taken_loc = [[False, False, False, False, False, False, False, False, False, False] for x in range(s2.row)]

        for r in s2.robots_loc: 
            if r.col < 0 or r.col > 10 or r.row < 0 or r.row > 5:
                return False 
            
            if r_taken_loc[r.row][r.col] == True: 
                return False 
            else: 
                r_taken_loc[r.row][r.col] = True

        s_taken_loc = [[False, False, False, False, False, False, False, False, False, False] for x in range(s2.row)]

        for s in s2.stacks_loc:
            if s_taken_loc[s.row][s.col] == True: 
                return False 
            else: 
                s_taken_loc[s.row][s.col] = True
        
        robot_pos1 = {}
        robot_pos2 = {}

        for index,l in enumerate(self.robots_loc): 
            robot_pos1[l.__repr__()] = s2.robots_loc[index].__repr__()
            robot_pos2[s2.robots_loc[index].__repr__()] = l.__repr__()
        
        for r in s2.robots_loc: 
            if r.__repr__() in robot_pos1.keys() and robot_pos1[r.__repr__()] == robot_pos2[r.__repr__()]:
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
        while possibleState == False: # run this function until possible state is true, this tells us that its possible to go to next state
            a = Actions(self.warehouse) # create random list of actions
            print(a)
            cs = self.calculate_state(a) # calculate new state
            print('calculated state', cs)
            ps = self.possible_state(cs) # see if new state is possible
            if ps == True: # if possible then set possible state = True and return list of actions.
                possibleState = ps
                return a

        # a = Actions(self.warehouse) # create random list of actions
        return a


    
    def update_cost(self):
        self.cost += sum(self.state.ordered)
        return
    
    def __repr__(self):
        return str(self.state) + "t = " + str(self.t) + ", cost = " + str(self.cost)
         

def main():
    w = Warehouse(5, 10, 10, 20, 0.25)
    print(w)
    
    x0 = State(w)
    print(x0)
    agent = Agent(w, x0)
    
    while(agent.t < 10):
        agent.state.order_items()
        agent.update_cost()
        agent.t += 1
        a = agent.policy()
        agent.state = agent.calculate_state(a)
        print(agent)
        agent.possible_state(agent)
    
main()







