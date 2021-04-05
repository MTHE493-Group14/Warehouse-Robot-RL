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
            self.df = pd.DataFrame([], columns=['time_steps', 'qval_rmse', 'avg_cost', 'max_avg_cost', 'min_avg_cost'])
            self.save(method, filename)
        else:
            self.df = pd.read_csv('Performance/' + method + '_' + filename + '.csv')
            
        return
    
    def update(self, time_steps, qval_rmse, avg_cost, max_avg_cost, min_avg_cost):
        """
        Update the performance dataframe with the latest score.

        Parameters
        ----------
        time_steps : int
            The total number of time steps in training.
        qval_rmse : float
            The sum of changes in Q-values.
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
            prev_time_steps = 0
        else:
            prev_time_steps = self.df.iloc[-1]['time_steps']
        add = { 'time_steps': prev_time_steps + time_steps, 
                'qval_rmse': qval_rmse, 
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
    
    def plot_cost(self):
        """
        Plot the cost of the greedy policy over training iterations.

        Returns
        -------
        None.

        """
        plt.xlabel('Time Steps')
        plt.ylabel('Cost Per Time Step')
        plt.plot(self.df['time_steps'], self.df['avg_cost'], c='blue')
        plt.plot(self.df['time_steps'], self.df['max_avg_cost'], c='orange')
        plt.plot(self.df['time_steps'], self.df['min_avg_cost'], c='green')
        plt.legend(['Average Cost', 'Max Average Cost', 'Min Average Cost'])
        plt.show()
        return

    def plot_RMSE(self):
        """
        Plot the RMSE of the change in Q-values over training iterations.

        Returns
        -------
        None.

        """
        plt.xlabel('Time Steps')
        plt.ylabel('Q-Value RMSE')
        plt.plot(self.df['time_steps'], self.df['qval_rmse'], c='red')
        plt.show()
        return