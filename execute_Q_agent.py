# Importing classes
from datetime import datetime
from maze import Environment
from Q_learning_algorithm import QTable
import csv

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

def get_user_input():
    print('Please enter your choice for environment')
    print('0. Exit')
    print('1. No Obstacle')
    print('2. One Obstacle')
    
    choose_envi = int(input('Please enter your choice:'))
    return choose_envi

# Commands to be implemented after running this file
if __name__ == "__main__":
    # Getting and checking user input
    while True:
        try:
            user_input = get_user_input()
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        
        if user_input > 2 or user_input < 0:
            print("Sorry, please choose 0, 1 or 2.")
            continue
        elif user_input == 0:
            exit()
        else:
            break
    
    
    # Calling for the environment
    env = Environment({ 'algo': 'Q-Learning', 'envi': envi_options[user_input-1]})

    ''' # Calling for the main algorithm
    RL = QTable(actions=list(range(env.total_actions)))
    # Running the main loop with Episodes by calling the function exec_update()
    env.after(100, exec_update(10))  # Or just exec_update()
    env.mainloop() '''

    # declaring head_routes_fields as heading in csv
    #head_routes_fields = ['Route']
    head_epsilon = ['']

    # declaring Q-table fields as heading
    head_qTable_fields = ['XXXXXX']

    # declaring rows for storing dynamic outputs
    #routes_rows = []
    short_rows = [] # table 1
    long_rows = [] # table 2
    time_rows = [] # table 3
    q_table_rows = [] # table 4
    
    routes_row_head = ['']
    q_table_row_head = ['']

    gamma_array = [0.9, 0.8, 0.7, 0.6, 0.5]
    epsilon_array = [0.9, 0.8, 0.7, 0.6, 0.5]
    
    # loop to create heading for each table
    for epsilon_item in range(len(epsilon_array)):
        # first row as epsilon values
        #head_routes_fields += epsilon_array[epsilon_item], '', '' # head_routes_fields = Short-long routes,0.6,'',0.5,''
        #routes_row_head += 'Short', 'Long', 'Time'

        # first row as epsilon values
        head_qTable_fields += epsilon_array[epsilon_item], '' # head_qTable_fields = Q-table | Final ,0.6,'',0.5,''
        q_table_row_head += 'Final', 'Full'

    #routes_rows += [routes_row_head]
    # append second row as titles 'Final' 'Full'
    q_table_rows += [q_table_row_head]


    for gamma_item in range(len(gamma_array)):
        
        # declalring shortest route array for storing all routes 
        # found using Combination of "one Gamma with multiple Epsilon"
        # short_long_routes = []
        
        # for one Gamma run 10 trials
        for trial in range(1,6):
            short_routes = [] # table 1
            long_routes = [] # table 2
            total_time = [] # table 3
            q_tables = [] # table 4
            for epsilon_item in range(len(epsilon_array)):
                print(gamma_array[gamma_item], epsilon_array[epsilon_item])
                
                # making Q-table ready for exploration
                RL = QTable( actions=list(range(env.total_actions)), gamma = gamma_array[gamma_item], epsilon = epsilon_array[epsilon_item] )
                
                # Running the main loop with Episodes by calling the function exec_update()
                #env.after(100, exec_update(10))  # Or just exec_update()
                shortest_route, longest_route, q_table_final, q_table, time_taken = exec_update(500)
                
                # storing all shortest route for each iteration to show in "row" format
                short_routes += [shortest_route] # table 1
                long_routes += [longest_route] # table 2
                total_time += [time_taken] # table 3
                q_tables += [q_table_final, q_table] # table 4

            
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

        # empty row to separate gamma trials 
        short_rows += [''] # table 1
        long_rows += [''] # table 2
        time_rows += [''] # table 3
        q_table_rows += [''] # table 4

    #print(head_routes_fields)
    #print(routes_rows)
    #end of execution
    
    epsilon_array.insert(0, 'X-X-X-X')
    date = datetime.now().strftime("%Y_%m_%d-%I_%M%p")

    with open("Q-Analysis_"+ envi_options[user_input-1] +"_"+date+".csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['', '' ,'Q Learning Algorithm', '', envi_options[user_input-1]])
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
        writer.writerows(q_table_rows)

    env.mainloop()