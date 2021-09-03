# Importing classes
from datetime import datetime
from maze import Environment
from Q_learning_algorithm import QTable
import csv
import time

shortest_route = 0
longest_route = 0

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


# Commands to be implemented after running this file
if __name__ == "__main__":
    # Calling for the environment
    env = Environment()
    '''  env = Environment()
    # Calling for the main algorithm
    RL = QTable(actions=list(range(env.total_actions)))
    # Running the main loop with Episodes by calling the function exec_update()
    env.after(100, exec_update(10))  # Or just exec_update()
    env.mainloop()
'''
    # declaring head_routes_fields as heading in csv
    head_routes_fields = ['Route']

    # declaring Q-table fields as heading
    head_qTable_fields = ['Q-Table']

    # declaring rows for storing dynamic outputs
    routes_rows = []
    q_table_rows = []
    routes_row_head = ['']
    q_table_row_head = ['']
    gamma_array = [0.7, 0.6]
    epsilon_array = [0.6, 0.5, 0.4]
    
    for epsilon_item in range(len(epsilon_array)):
        # first row as epsilon values
        head_routes_fields += epsilon_array[epsilon_item], '', '' # head_routes_fields = Short-long routes,0.6,'',0.5,'' 
        routes_row_head += 'Short', 'Long', 'Time'

        # first row as epsilon values
        head_qTable_fields += epsilon_array[epsilon_item], '' # head_qTable_fields = Q-table | Final ,0.6,'',0.5,''
        q_table_row_head += 'Final', 'Full'

    routes_rows += [routes_row_head]
    q_table_rows += [q_table_row_head]


    for gamma_item in range(len(gamma_array)):
        #set header for writing in CSV file - header will epsilon value
        
        epsilon_temp = 0
        
        # declalring shortest route array for storing all routes 
        # found using Combination of "one Gamma with multiple Epsilon"
        short_long_routes = []
        q_tables = []
        for epsilon_item in range(len(epsilon_array)):
            print(gamma_array[gamma_item], epsilon_array[epsilon_item])
            
            # making Q-table ready for exploration
            RL = QTable( actions=list(range(env.total_actions)), gamma = gamma_array[gamma_item], epsilon = epsilon_array[epsilon_item] )
            
            # Running the main loop with Episodes by calling the function exec_update()
            #env.after(100, exec_update(10))  # Or just exec_update()
            shortest_route, longest_route, q_table_final, q_table, time_taken = exec_update(10)
            
            # storing all shortest route for each iteration to show in "row" format
            short_long_routes += [shortest_route, longest_route, time_taken]

            # storing all shortest route for each iteration to show in "row" format
            q_tables += [q_table_final, q_table]

        
        # add "first" element as "Gamma" value for each row
        short_long_routes.insert(0, gamma_array[gamma_item])

        # collecting rows
        routes_rows += [short_long_routes]

        # -----------------------------------------------------------
        # ----------------------- q table rows ----------------------
        # -----------------------------------------------------------
        
        # add "first" element as "Gamma" value for each row
        q_tables.insert(0, gamma_array[gamma_item])

        # collecting rows
        q_table_rows += [q_tables]

    print(head_routes_fields)
    print(routes_rows)
    #end of execution
    env.mainloop()
    
    with open('analysis.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(head_routes_fields)
        writer.writerows(routes_rows)

        writer.writerow('')
        
        writer.writerow(head_qTable_fields)
        writer.writerows(q_table_rows)
        
