# Importing classes
from datetime import datetime
from maze import Environment
from SARSA_learning_algorithm import SarsaTable
import csv
from generate_csv import generate_csv

shortest_route = 0
longest_route = 0
envi_options = ['no-obstacle', 'Obstacle']

def exec_update(iterations = 1000):
    # Resulted list for the plotting Episodes via Steps
    steps = []
    start_time = datetime.now()
    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(iterations): # also works with 100 iterations
        # Initial Observation
        observation = env.reset()

        # Updating number of Steps for each Episode
        i = 0

        # Updating the cost for each episode
        cost = 0

        # RL choose action based on observation
        action = RL.choose_action(str(observation))

        while True:
            # Refreshing environment
            env.render()

            # RL takes an action and get the next observation and reward
            observation_, reward, done = env.step(action)

            # RL choose action based on next observation
            action_ = RL.choose_action(str(observation_))

            # RL learns from the transition and calculating the cost
            cost += RL.learn(str(observation), action, reward, str(observation_), action_)

            # Swapping the observations and actions - current and next
            observation = observation_
            action = action_

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
    
    print("total time:",datetime.now() - start_time)

    # Showing the Q-table with values for each action
    #RL.print_q_table()
    # Plotting the results
    #RL.plot_results(steps, all_costs)

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
    from user_choice import *

    environment_name = envi_options[user_input-1]
    algorithm_name = 'SARSA'
    # Calling for the environment
    env = Environment({ 'algo': algorithm_name+'-Learning', 'envi': environment_name})

    # execution setting variables
    max_trials = 2 # 11
    num_of_episodes = 10 #1000
    gamma_array = [0.9]#, 0.8, 0.7, 0.6, 0.5]
    epsilon_array = [0.9]#, 0.8, 0.7, 0.6, 0.5]

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

    for epsilon_item in range(len(epsilon_array)):
        # first row as epsilon values
        head_qTable_fields += epsilon_array[epsilon_item], '' # head_qTable_fields = Q-table | Final ,0.6,'',0.5,''
        q_table_row_head += 'Final', 'Full'

    q_table_rows += [q_table_row_head]

    # Execution start ---
    for gamma_item in range(len(gamma_array)):
        # short_long_routes = []
        trial_short_routes_rows = []
        trial_long_routes_rows = []
        trial_time_rows = []
        # for one Gamma run 10 trials
        for trial in range(1, max_trials):
            short_routes = [] # table 1
            long_routes = [] # table 2
            total_time = [] # table 3
            q_tables = [] # table 4
            for epsilon_item in range(len(epsilon_array)):
                print(gamma_array[gamma_item], epsilon_array[epsilon_item])
                
                # making Q-table ready for exploration
                RL = SarsaTable( actions=list(range(env.total_actions)), gamma = gamma_array[gamma_item], epsilon = epsilon_array[epsilon_item], learning_rate=0.1 )
                
                # Running the main loop with Episodes by calling the function exec_update()
                shortest_route, longest_route, q_table_final, q_table, time_taken = exec_update(num_of_episodes)
                
                # storing all shortest route for each iteration to show in "row" format
                short_routes += [shortest_route] # table 1
                long_routes += [longest_route] # table 2
                total_time += [time_taken] # table 3
                q_tables += [q_table_final, q_table] # table 4
            
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

        # collecting rows for AVERAGE file TABLE
        average_short_routes = get_trial_average(trial_short_routes_rows)
        average_short_rows += [average_short_routes]
        
        average_long_routes = get_trial_average(trial_long_routes_rows)
        average_long_rows += [average_long_routes]
        
        average_time = get_trial_average(trial_time_rows)
        average_time_rows += [average_time]

        # empty row to separate gamma bulk-trial 
        short_rows += [''] # table 1
        long_rows += [''] # table 2
        time_rows += [''] # table 3
        q_table_rows += [''] # table 4

    # end of execution -----

    create_csv = generate_csv()
    create_csv.generate(algorithm_name, environment_name, epsilon_array, short_rows, long_rows, time_rows, head_qTable_fields, q_table_rows)
    create_csv.generate_avg(algorithm_name, environment_name, epsilon_array, average_short_rows, average_long_rows, average_time_rows)
    '''with open("SARSA_analysis_"+ envi_options[user_input-1] +"_"+date+".csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['', '' ,'SARSA Learning Algorithm', '', envi_options[user_input-1]])
        writer.writerow('')

        # print shortest path table
        writer.writerow(['','Shortest Path'])
        writer.writerow(epsilon_array)
        writer.writerows(short_rows)
        writer.writerow('')

        # print longest path table 
        writer.writerow(['','Longest Path'])
        writer.writerow(epsilon_array)
        writer.writerows(long_rows)
        writer.writerow('')

        # print 'time' table
        writer.writerow(['','Total time'])
        writer.writerow(epsilon_array)
        writer.writerows(time_rows)
        writer.writerow('')

        # print Q table
        writer.writerow(['','Q Table'])
        writer.writerow(head_qTable_fields)
        writer.writerows(q_table_rows)'''

    env.mainloop()