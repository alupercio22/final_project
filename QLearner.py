from player import Player
from variables import Variables
import numpy as np
import pandas as pd


class Qlearning(Player):
    def __init__(self):
        super().__init__()
        self.Q_Values = {}
        self.endState = None
        self.last_action = None
        self.lr = .7
        self.disc = .9
        self.eps = .9
        self.learning = True

    def resetCards(self):
        self.cards = []
        self.endState = None
        self.last_action = None
    
    def getAction(self, state):
        if state in self.Q_Values and np.random.uniform(0,1) < self.eps:
            action = max(self.Q_Value[state], key = self.Q_Values[state].get)
        else:
            action = np.random.choice([Variables.hit, Variables.stay])

            if state not in self.Q_Values:
                self.Q_Values[state] = {}
            
            self.Q_Values[state][action] = 0
        
        self.endState = state
        self.last_action = action

        return action
    
    def update(self, newState, reward):
        if self.learning:
            previous = self.Q_Values[self.endState][self.last_action]

            if newState in self.Q_Values:
                new = self.disc * self.Q_Values[newState][max(self.Q_Values[newState], key=self.Q_Values[newState].get)]
            
            else:
                new = 0
            
            self.Q_Values[self.endState][self.last_action] = (1-self.lr)*previous + self.lr*(reward+new)

    def best_strategy(self):
        bestStrat_df = pd.DataFrame(self.Q_Values).transpose()
        bestStrat_df['best'] = bestStrat_df.apply(lambda x : 'hit' if x['hit'] > x['stay'] else 'stay', axis=1)
        return bestStrat_df