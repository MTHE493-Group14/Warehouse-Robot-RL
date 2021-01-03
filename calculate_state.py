    import copy

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