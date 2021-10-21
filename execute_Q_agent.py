# Importing classes
import numpy as np
from datetime import datetime
from maze import Environment
from Q_learning_algorithm import QTable
import time
from generate_csv import generate_csv
from user_choice import user_choice_class

shortest_route = 0
longest_route = 0


def exec_update(iterations = 1000):
    # Resulted list for the plotting Episodes via Steps
    steps = []
    start_time = datetime.now()
    shortest_route = 0
    longest_route = 0
    # Summed costs for all episodes in resulted list
    all_costs = []
    for episode in range(iterations): # also works with 100 iterations
        # Initial Observation
        observation = env.reset()
    
        # Updating number of Steps for each Episode
        i = 0

        # Updating the cost for each episode
        cost = 0

        while True:
            # Refreshing environment
            env.render()

            # RL chooses action based on observation
            action = RL.choose_action(str(observation))
            
            # RL takes an action and get the next observation and reward
            observation_, reward, done = env.step(action)

            # RL learns from this transition and calculating the cost
            cost += RL.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
            observation = observation_

            # Calculating number of Steps in the current Episode
            i += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
            if done:
                steps += [i]
                all_costs += [cost]
                break
            
    # Showing the final route
    shortest_route, longest_route = env.final()
    
    # Showing the Q-table with values for each action
    q_table_final, q_table = RL.print_q_table()

    # Plotting the results
    # RL.plot_results(steps, all_costs)
    #env.clearFoundPath() 
    time_taken = datetime.now() - start_time
    print('Shortest: ', shortest_route, ' | Longest path: ', longest_route)
    print('Final Q Table: ', q_table_final, ' | Q Table: ', q_table)
    print("total time:", time_taken)

    return shortest_route, longest_route, q_table_final, q_table, time_taken

# get trial average of array
def get_trial_average(trial_short_routes_rows):
    # filter array to remove empty element
    temp_a = np.array(list(filter(None,trial_short_routes_rows)))
    # convert row to column
    converted = temp_a.transpose()
    # average of each column
    average_a = (np.mean(converted, axis=1)).tolist()
    return average_a

# Commands to be implemented after running this file
if __name__ == "__main__":

    # Getting and checking user input
    u_choice = user_choice_class()
    environment_name = u_choice.get_selected_envi() # fetch user selected environment
    
    algorithm_name = 'Q'
    # Calling for the environment
    env = Environment({ 'algo': algorithm_name+'-Learning', 'envi': environment_name})

    # execution setting variables
    max_trials = 5 # 11
    num_of_episodes = 1000 # 1000
    gamma_array = [0.85] # discount factor
    epsilon_array = [0.9, 0.8] # epsilon decay

    learning_rate = 0.01
    if(environment_name == 'Cliff Walk'):
        learning_rate = 0.5
         
    # declaring head_routes_fields as heading in csv
    head_epsilon = ['']
    
    # declaring Q-table fields as heading
    head_qTable_fields = ['XXXXXX']

    # declaring rows for storing dynamic outputs
    #routes_rows = []
    short_rows = [] # table 1
    long_rows = [] # table 2
    time_rows = [] # table 3
    q_table_rows = [] # table 4
    
    average_short_rows = [] # average-csv Table 1
    average_long_rows = [] # average-csv Table 2
    average_time_rows = [] # average-csv Table 2

    q_table_row_head = ['']
    
    # loop to create heading for each table
    for epsilon_item in range(len(epsilon_array)):
        # first row as epsilon values
        head_qTable_fields += epsilon_array[epsilon_item], '' # head_qTable_fields = Q-table | Final ,0.6,'',0.5,''
        q_table_row_head += 'Final', 'Full'

    # append second row as titles 'Final' 'Full'
    q_table_rows += [q_table_row_head]

    # Execution start ---
    for gamma_item in range(len(gamma_array)):
        # short_long_routes = []
        trial_short_routes_rows = []
        trial_long_routes_rows = []
        trial_time_rows = []
        # for one Gamma run 10 trials
        for trial in range(0, max_trials):
            print("-- Trial -- ", trial+1)
            short_routes = [] # table 1
            long_routes = [] # table 2
            total_time = [] # table 3
            q_tables = [] # table 4
            for epsilon_item in range(len(epsilon_array)):
                print(gamma_array[gamma_item], epsilon_array[epsilon_item])
                
                # making Q-table ready for exploration
                RL = QTable( actions=list(range(env.total_actions)), gamma = gamma_array[gamma_item], epsilon = epsilon_array[epsilon_item], learning_rate = learning_rate)
                
                time.sleep(1.5)
                # Running the main loop with Episodes by calling the function exec_update()
                #env.after(100, exec_update(10))  # Or just exec_update()
                short_route, long_route, final_q_table, full_q_table, total_time_taken = exec_update(num_of_episodes)
                
                # storing all shortest route for each iteration to show in "row" format
                short_routes += [short_route] # table 1
                long_routes += [long_route] # table 2
                total_time += [total_time_taken] # table 3
                q_tables += [final_q_table, full_q_table] # table 4

            # END epsilon loop -----
            
            # Average of trials: Collecting rows ---START---
            trial_short_routes_rows += [short_routes]
            trial_long_routes_rows += [long_routes]
            trial_time_rows += [total_time]
            # Average of trials ---END---

            
            # add "first" element as "Gamma" value for each row
            #short_long_routes.insert(0, gamma_array[gamma_item])
            short_routes.insert(0, gamma_array[gamma_item]) # table 1... 0.9 __ __ __ __
            long_routes.insert(0, gamma_array[gamma_item]) # table 2... 0.9 __ __ __ __
            total_time.insert(0, gamma_array[gamma_item]) # table 3... 0.9 __ __ __ __
            q_tables.insert(0, gamma_array[gamma_item]) # table 4... 0.9 __ __ __ __

            # collecting rows
            # routes_rows += [short_long_routes]
            short_rows += [short_routes] # table 1
            long_rows += [long_routes] # table 2
            time_rows += [total_time] # table 3
            q_table_rows += [q_tables] # table 4

        # END trial loop -----

        # collecting rows for AVERAGE file TABLE ---START---
        average_short_routes = get_trial_average(trial_short_routes_rows)
        average_short_rows += [average_short_routes]
        
        average_long_routes = get_trial_average(trial_long_routes_rows)
        average_long_rows += [average_long_routes]
        
        average_time = get_trial_average(trial_time_rows)
        average_time_rows += [average_time]
        # collecting rows for AVERAGE file TABLE ---END---

        # empty row to separate gamma trials 
        short_rows += [''] # table 1
        long_rows += [''] # table 2
        time_rows += [''] # table 3
        q_table_rows += [''] # table 4

    # end of execution -----
    epsilon_array.insert(0, 'X-X-X-X')
    create_csv = generate_csv()
    create_csv.generate(algorithm_name, environment_name, epsilon_array, short_rows, long_rows, time_rows, head_qTable_fields, q_table_rows, num_of_episodes)

    create_csv.generate_avg(algorithm_name, environment_name, epsilon_array, average_short_rows, average_long_rows, average_time_rows, num_of_episodes)

    env.mainloop()