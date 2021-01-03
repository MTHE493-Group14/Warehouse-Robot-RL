 def possible_state(self, s2):
        """
        Checks if transitioning from the agent's current state to a new state is possible 
        
        Check if robots are outside the grid in state2 
        Check if 2 robots are in the same location in state2 
        Check if 2 stacks are in the same location in state2 
        Check if 2 robots moved through one another (I.e. switched locations transitioning from the current state to state2)
        Return a boolean value if its available 
        """
        r_taken_loc = [[False, False, False, False, False, False, False, False, False, False] for x in range(s2.row)] #Makes a 5x10 grid with all inputs as False

        for r in s2.robots_loc: 
            if r.col < 0 or r.col > 10 or r.row < 0 or r.row > 5: #Checks if robots are outside grid in state 2
                return False 
            
            if r_taken_loc[r.row][r.col] == True: #Checks if 2 robots are in the same location in state 2, if the slot of the grid is already true, then a robot is present
                return False 
            else: 
                r_taken_loc[r.row][r.col] = True #Replace each robot location in state 2 with true in the 5x10 grid 

        s_taken_loc = [[False, False, False, False, False, False, False, False, False, False] for x in range(s2.row)] #Makes a 5x10 grid with all inputs as False 

        for s in s2.stacks_loc:
            if s_taken_loc[s.row][s.col] == True: #Checks if 2 stacks are in the same location in state 2, if the slot of the grid is already true, then a stack is present
                return False 
            else: 
                s_taken_loc[s.row][s.col] = True #Replace each stack location in state 2 with true in the 5x10 grid
        
        robot_pos1 = {} #Dictionary that maps State 1 locations to state 2 locations
        robot_pos2 = {} #Dictionary that maps State 2 locations to state 1 locations

        for index,l in enumerate(self.robots_loc): 
            robot_pos1[l.__repr__()] = s2.robots_loc[index].__repr__()
            robot_pos2[s2.robots_loc[index].__repr__()] = l.__repr__()
        
        for r in s2.robots_loc: 
            if r.__repr__() in robot_pos1.keys() and robot_pos1[r.__repr__()] == robot_pos2[r.__repr__()]: #Checks if 2 robots switched locations
                return False

        return True