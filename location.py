class Location:
    """
    Location objects represent the grid coordinates of a warehouse robot or 
    inventory stack.
    
    Attributes
    ----------
    row : int
        The row of the cell that the robot or stack is located in.
    col : int
        The column of the cell that the robot or stack is located in.
    
    """
    
    def __init__(self, row, col):
        """
        Creates a new Location object given a set of coordinates.

        Parameters
        ----------
        row : int
            The row of the cell that the robot or stack is located in.
        col : int
            The column of the cell that the robot or stack is located in.

        Returns
        -------
        None.

        """
        self.row = row
        self.col = col
        return
    
    def __eq__(self, other):
        """
        Given another Location object, determine if the locations are the same.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indication if the locations are equal.

        """
        return self.row == other.row and self.col == other.col
    
    def __lt__(self, other):
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col < other.col
        else:
            return False
    
    def __le__(self, other):
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col <= other.col
        else:
            return False
    
    def __gt__(self, other):
        if self.row > other.row:
            return True
        elif self.row == other.row:
            return self.col > other.col
        else:
            return False
    
    def __ge__(self, other):
        if self.row > other.row:
            return True
        elif self.row == other.row:
            return self.col >= other.col
        else:
            return False
    
    def __ne__(self, other):
        return self.row != other.row or self.col != other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __repr__(self):
        """
        Return the string representation of a Location object. 

        Returns
        -------
        str
            The string representation of a Location object.

        """
        return "(" + str(self.row) + ", " + str(self.col) + ")"