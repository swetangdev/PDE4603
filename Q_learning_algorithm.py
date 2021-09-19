# Q-learning algorithm 

# initialize Q-table > choose an action > perform an action > Measure Reward > Update Q-Table
#                           ^ ------------------------------------------------------|  

import numpy as np
import pandas as pd

from maze import final_states

class QTable:
    def __init__(self, actions, gamma = 0.9, epsilon = 0.9, learning_rate = 0.01):
        self.actions = actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_rate = learning_rate

        # Q-table for exploration
        self.q_table = pd.DataFrame(columns = self.actions, dtype=np.float64)
        
        # final route Q-table
        self.q_table_final = pd.DataFrame(columns = self.actions, dtype=np.float64)
        

    # function to choose an action 
    def choose_action(self, observation):
        # Checking if the state exists in the table
        self.is_state_exist(observation)
        # Selection of the action - 90 % according to the epsilon == 0.9
        # Choosing the best action
        if np.random.uniform() < self.epsilon:
            # choose action via exploitation
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            # Choosing random action - left 10 % for choosing randomly
            # choose action via exploration
            action = np.random.choice(self.actions)
        return action

    # function for learn Q-table as well as update Q-table
    # Q-function Q(s,a) = Q(s,a) + lr * ( R(s,a) + gamma * max[ Q(s',a') ] - Q(s,a) )
    def learn(self, state, action, reward, next_state):
        self.is_state_exist(next_state)

        # Q(s,a) Current state in the current position
        q_predict = self.q_table.loc[state, action]

        # Checking if the next state - Q(s',a') - is open OR (it is obstacle or goal)
        if next_state != 'goal' or next_state != 'obstacle':
            q_target = reward + self.gamma * self.q_table.loc[next_state, :].max()
        else:
            q_target = reward

        # Updating Q-table with new knowledge
        self.q_table.loc[state, action] += self.learning_rate * (q_target - q_predict)

        return self.q_table.loc[state, action]

    def is_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series([0]*len(self.actions), index = self.q_table.columns, name = state)
            )

    # Printing the Q-table with states
    def print_q_table(self):
        # Getting the coordinates of final route from env.py
        e = final_states()

        # Comparing the indexes with coordinates and writing in the new Q-table values
        for i in range(len(e)):
            state = str(e[i])  # state = '[5.0, 40.0]'
            # Going through all indexes and checking
            for j in range(len(self.q_table.index)):
                if self.q_table.index[j] == state:
                    self.q_table_final.loc[state, :] = self.q_table.loc[state, :]

        #print()
        #print('Length of final Q-table =', len(self.q_table_final.index))
        #print('Final Q-table with values from the final route:')
        #print(self.q_table_final)

        #print()
        #print('Length of full Q-table =', len(self.q_table.index))
        #print('Full Q-table:')
        #print(self.q_table)

        return len(self.q_table_final.index), len(self.q_table.index)