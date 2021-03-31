from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
from QLearner import Qlearning
from player import Player
from variables import Variables
import numpy as np
import pandas as pd


class DQNLearner(Qlearning):
    def __init__(self):
        super().__init__()
        self.lr = .5
        self.disc = .1
        self.eps = .9
        self.learning = True

        model = Sequential()

        model.add(Dense(2, kernel_initializer='lecun_uniform', input_shape=(2,)))
        model.add(Activation('relu'))

        model.add(Dense(10, kernel_initializer='lecun_uniform'))
        model.add(Activation('relu'))

        model.add(Dense(4, kernel_initializer='lecun_uniform'))
        model.add(Activation('linear'))

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)

        self.bjackModel = model


    def getAction(self, state):
        rewards = self.bjackModel.predict([np.array([state])], batch_size=1)

        if np.random.uniform(0,1) < self.eps:
            if rewards[0][0] > rewards[0][1]:
                action = Variables.hit
            else:
                action = Variables.stay
        else:
            action = np.random.choice([Variables.hit, Variables.stay])

        self.end_state = state
        self.last_action = action
        self.lastReward = rewards


        return action

    def update(self,new_state,reward):
        if self.learning:
            rewards = self.bjackModel.predict([np.array([new_state])], batch_size=1)
            maxQ_Value = rewards[0][0] if rewards[0][0] > rewards[0][1] else rewards[0][1]
            new = self.disc * maxQ_Value

            if self.last_action == Variables.hit:
                self.lastReward[0][0] = reward+new
            else:
                self.lastReward[0][1] = reward+new

            # Update
            #self.bjackModel.fit(np.array([self.endState]), self.lastReward, batch_size=1, epochs=1, verbose=0)

    def get_optimal_strategy(self):
        
        index = []
        for x in range(4,21):
            for y in range(2,12):
                index.append((x,y))
        
        bestStrat_df = pd.DataFrame(index = index, columns = ['hit', 'stay'])

        for ind in index:
            outcome = self.bjackModel.predict([np.array([ind])], batch_size=1)
            bestStrat_df.iloc[ind, 0] = outcome[0][0]
            bestStrat_df.iloc[ind, 1] = outcome[0][1]


        bestStrat_df['optimal'] = bestStrat_df.apply(lambda x : 'hit' if x['hit'] >= x['stay'] else 'stay', axis=1)
        return bestStrat_df
