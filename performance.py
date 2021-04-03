import pandas as pd
import matplotlib.pyplot as plt

class Performance:
    """
    Track the performance of the greedy policy throughout training.
    
    performance : Pandas DataFrame
        A dataframe indicating the performance of the greedy policy after 
        training for some number of iterations.
    """
    
    def __init__(self, method, filename, overwrite):
        """
        Initialize the performance dataframe.

        Parameters
        ----------
        filename : str
            The filename that should be used to read/write the dataframe.
        overwrite : bool
            Whether or not the dataframe should be overwritten by a new one. 

        Returns
        -------
        None.

        """
        if overwrite:
            self.df = pd.DataFrame([], columns=['iterations', 'avg_cost', 'max_avg_cost', 'min_avg_cost'])
            self.save(method, filename)
        else:
            self.df = pd.read_csv('Performance/' + method + '_' + filename + '.csv')
            
        return
    
    def update(self, iters, avg_cost, max_avg_cost, min_avg_cost):
        """
        Update the performance dataframe with the latest score.

        Parameters
        ----------
        iters : int
            The total number of iterations performed in training.
        avg_cost : float
            The average cost when following the greedy policy.
        max_avg_cost : int
            The max average cost when following the greedy policy.
        min_avg_cost : int
            The min average cost when following the greedy policy.

        Returns
        -------
        None.

        """
        if len(self.df) == 0:
            old_iters = 0
        else:
            old_iters = self.df.iloc[-1]['iterations']
        add = { 'iterations': iters + old_iters, 
                'avg_cost': avg_cost, 
                'max_avg_cost': max_avg_cost, 
                'min_avg_cost': min_avg_cost}
        self.df = self.df.append(add, ignore_index=True)
        
        return
    
    def save(self, method, filename):
        """
        Save the performance dataframe.

        Parameters
        ----------
        filename : str
            The filename that should be used to read/write the dataframe.

        Returns
        -------
        None.

        """
        self.df.to_csv('Performance/' + method + '_' + filename + '.csv', index=False)
        return
    
    def plot(self):
        """
        Plot the performance of the greedy policy over training iterations.

        Returns
        -------
        None.

        """
        plt.xlabel('Iterations')
        plt.ylabel('Cost Per Timestep')
        plt.plot(self.df['iterations'], self.df['avg_cost'], c='blue')
        plt.plot(self.df['iterations'], self.df['max_avg_cost'], c='red')
        plt.plot(self.df['iterations'], self.df['min_avg_cost'], c='green')
        plt.legend(['Average Cost', 'Max Average Cost', 'Min Average Cost'])
        plt.show()
        return