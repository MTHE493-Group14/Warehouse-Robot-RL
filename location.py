class Location:
    """
    Location objects represent the grid coordinates of a warehouse robot or 
    inventory stack.
    
    In order to reduce the size of the state space, we need to define a way to
    order the Locations. The __eq__, __lt__, __le__, __gt__, __ge__, and 
    __ne__ methods define the order. The display below provides an example as 
    to how the locations are ordered.
    
    -------------------
    |  1  |  2  |  3  |
    -------------------
    |  4  |  5  |  6  |
    -------------------
    |  7  |  8  |  9  |
    -------------------
    
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
        Given another Location object, determine if the two locations are the 
        same.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if the locations are equal.

        """
        return self.row == other.row and self.col == other.col
    
    def __lt__(self, other):
        """
        Given another Location object, determine if this location is ordered 
        before the other location.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if this location is ordered before the 
            other location.

        """
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col < other.col
        else:
            return False
    
    def __le__(self, other):
        """
        Given another Location object, determine if this location is ordered 
        before the other location or if the locations are equal.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if this location is ordered before the 
            other location or if the locations are equal.

        """
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col <= other.col
        else:
            return False
    
    def __gt__(self, other):
        """
        Given another Location object, determine if this location is ordered 
        after the other location.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if this location is ordered after the 
            other location.

        """
        if self.row > other.row:
            return True
        elif self.row == other.row:
            return self.col > other.col
        else:
            return False
    
    def __ge__(self, other):
        """
        Given another Location object, determine if this location is ordered 
        after the other location or if the locations are equal.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if this location is ordered after the 
            other location or if the locations are equal.

        """
        if self.row > other.row:
            return True
        elif self.row == other.row:
            return self.col >= other.col
        else:
            return False
    
    def __ne__(self, other):
        """
        Given another Location object, determine if the two locations are not
        the same.

        Parameters
        ----------
        other : Location
            Another Location object to compare to.

        Returns
        -------
        bool
            A boolean value indicating if the locations are not equal.
        
        """
        return self.row != other.row or self.col != other.col
    
    def __hash__(self):
        """
        Returns a hash value. This method is needed so that Locations can be
        grouped together in sets.

        Returns
        -------
        int
            A hash value for the Location object.

        """
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