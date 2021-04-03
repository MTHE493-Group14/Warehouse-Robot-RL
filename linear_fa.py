import numpy as np
import pickle

from state import State
from actions import Actions
from warehouse_parameters import N_ROWS, N_COLS, N_ROBOTS, N_STACKS, N_ITEMS, N_ACTIONS, DISCOUNT

class LinearFA:
    
    def __init__(self, filename, overwrite):
        if overwrite:
            s = State()
            a = Actions()
            self.w = np.random.rand(len(s.features2()) * len(a.features2()))
            self.tau = np.ones(len(self.w))
            
            total = 0
            iters = 1000
            for i in range(iters):
                s = State()
                s.orders = list(np.random.choice([0, 1], N_STACKS))
                a = Actions()
                f = self.combine_features(s.features2(), a.features2())
                total += np.sum(np.power(f, 2))
            self.x_norm = total / iters
            
            a.set_by_enum(0)
            self.Xa = [a.features2()]
            for i in range(1, N_ACTIONS ** N_ROBOTS):
                a.set_by_enum(i)
                self.Xa = np.concatenate((self.Xa, [a.features2()]), axis=0)
            self.Xa = self.Xa[:, :, np.newaxis]

            self.save(filename)
        else:
            self.load(filename)
        return
    
    def combine_features(self, sf, af):
        return np.multiply(af.reshape(-1, 1), sf).reshape(1, -1)
        
    def combine_features_all_actions(self, sf):
        return np.multiply(self.Xa, sf).reshape(N_ACTIONS ** N_ROBOTS, -1)
    
    def update(self, s1, s2, a, c):
        X1 = self.combine_features(s1.features2(), a.features2())
        X2 = self.combine_features_all_actions(s2.features2())
        
        pred1 = self.predict(X1)[0]
        min_pred2 = np.min(self.predict(X2))
        
        self.tau += X1[0]
        alpha = 1 / (self.tau * self.x_norm)
        self.w += alpha * (c + DISCOUNT*min_pred2 - pred1) * X1[0]
        return
    
    def predict(self, X):
        return np.dot(X, self.w)
    
    def load(self, filename):
        with open('Models/model_' + filename + '.pkl', 'rb') as file:
            lfa_dict = pickle.load(file)
        self.w = lfa_dict['w']
        self.tau = lfa_dict['tau']
        self.x_norm = lfa_dict['x_norm']
        self.Xa = lfa_dict['Xa']
        return
    
    def save(self, filename):
        lfa_dict = {'w': self.w, 
                    'tau': self.tau, 
                    'x_norm': self.x_norm, 
                    'Xa': self.Xa}
        with open('Models/model_' + filename + '.pkl', 'wb') as file:
            pickle.dump(lfa_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
        return
    
    def __repr__(self):
        return str(self.w)