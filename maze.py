# The MAZE environment

import numpy as np  # for data manipulation in matrix form
import tkinter as tk # for making GUI
import time # for time calculation
from PIL import Image, ImageTk
from numpy.core.records import array
from user_choice import envi_options

# define the size of an environment, 12 x 12 maze with each of 20 pixels
pixels = 40
# self.env_height = 12
# self.env_width = 12
# self.total_env_height = self.env_height * pixels
# self.total_env_width = self.env_width * pixels


# Global variable for dictionary with coordinates for the final route
a = {}
environment_name = ''

# class for environment 

class Environment(tk.Tk, object):
    def __init__(self, field = ({'algo': 'R-Learning', 'envi':''})):
        super(Environment, self).__init__()
        self.actions = ['up','down','left','right']
        self.obstacle_walls = []
        self.flagLocation = [pixels * 6, pixels * 6]
        
        # using ternary condition check if Algo, Envi options are exist or set it default value
        field['algo'] = 'R-Learning' if 'algo' not in field else field['algo']
        field['envi'] = envi_options[0] if 'envi' not in field else field['envi']
        
        print('Chosen Environment: ', field['envi'])
        
        self.title(field['algo'] + ' - Environment')
        
        
        # set chosen environment
        self.chosen_envi = field['envi']
        
        if self.chosen_envi == ''  or self.chosen_envi == envi_options[0] or self.chosen_envi == envi_options[1] or self.chosen_envi == envi_options[2]: # 'Obstacle' 'Obstacle Pipe'
            self.env_height = 9
            self.env_width = 9
            if self.chosen_envi == envi_options[2]:
                self.agentLocation = [0,0]
            else:
                self.agentLocation = [0,4]
        elif self.chosen_envi == 'Cliff Walk':
            self.env_height = 6
            self.env_width = 12
            self.agentLocation = [0,0]
        else:
            self.env_height = 12
            self.env_width = 12
            self.agentLocation = [0,0]

        self.total_env_height = self.env_height * pixels
        self.total_env_width = self.env_width * pixels
        self.total_actions = len(self.actions)
        self.geometry('{0}x{1}'.format(self.total_env_width, self.total_env_height))
        self.create_environment()

        # dictionaries for final route
        self.d = {}
        self.f = {}

        # key for dictionaries
        self.i = 0

        # writing final dictionaries first time
        self.c = True

        # longest route
        self.longest = 0

        # shotest route
        self.shortest = 0

    # creating an environment
    def create_environment(self):
        self.canvas_widget = tk.Canvas(self,  bg='white', height = self.total_env_height, width= self.total_env_width)

        # Creating grid lines
        for column in range(0, self.env_width * pixels, pixels):
            x0, y0, x1, y1 = column, 0, column, self.env_width * pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, self.env_height * pixels, pixels):
            x0, y0, x1, y1 = 0, row, self.env_width * pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

        

        # An array to help with building rectangles
        self.o = np.array([pixels / 2, pixels / 2])

        # check if user has chosen obstacle environment, then add obstacle to environment
        if self.chosen_envi == envi_options[0]: #'Obstacle'
            obstacle_coords = [[4,4]]
            self.obstacle_function(obstacle_coords, '#36b38b')
        if self.chosen_envi == envi_options[1]: #'Obstacle Pipe'
            obstacle_coords = [[4,2], [4,3], [4,4], [4,5], [4,6]]
            self.obstacle_function(obstacle_coords, '#36b38b')
        elif self.chosen_envi == envi_options[2]: #'In-Path Obstacle':
            obstacle_coords = [[0,2], [1,4], [2,1], [2,6], [3,4], [5,2], [4,0], [4,6], [6,4]]
            self.obstacle_function(obstacle_coords, 'purple')
        # elif self.chosen_envi == envi_options[3]: #'Obstacle Cross':
        #     #img_obstacle1 = Image.open("images/square.png")
        #     #self.obstacle1_object = ImageTk.PhotoImage(img_obstacle1)
        #     #self.obstacle1 = self.canvas_widget.create_image(pixels * 5, pixels * 5, anchor='nw', image=self.obstacle1_object)

        #     # obstacle envi 2
        #     # Obstacle Wall co ordinates for the maze
        #     '''obstacle_coords = [ [8,2], [9,3],
        #         [4,1], [3,2], [5,5], [6,4],
        #         [9,6], [6,7], [7,8], [1,7], [2,6],
        #         [5,10], [6,11], [10,7]]'''
        #     obstacle_coords = [[5,1], [8,2], [9,3], [9,1], [10,2],
        #         [1,2], [2,4], [1,5], [2,3], [5,5], [6,4],
        #         [9,6], [6,7], [7,8], [2,8], [3,7],
        #         [4,11], [5,10], [6,11], [11,7], [11,4]]
        #     # render obstacle block using dynamic function
        #     self.obstacle_function(obstacle_coords, '#36b38b')
        # elif self.chosen_envi == envi_options[4]: #Obstacle Walls
            
        #     # obstacle envi 2
        #     # Obstacle Wall co ordinates for the maze
        #     '''obstacle_coords = [[2,2], [3,2], [4,2], [4,3],
        #         [8,2], [8,3], [8,4], [9,4], [10,4],
        #         [1,5], [1,6], [2,6], [3,6],
        #         [2,9], [3,9], [4,9], [4,10],
        #         [7, 7], [7,8], [8,7], [7,9]]'''
        #     obstacle_coords = [[2,2], [3,2], [3,3], [4,2],
        #         [8,0], [8,1], [7,1], 
        #         [6,4], [7,4], [8,4],
        #         [2,6], [3,6],
        #         [4,10], [4,11], 
        #         [1,9],
        #         [7, 7], [7,8], [8,7], [7,9], [10,7]]
        #     # render obstacle block using dynamic function
        #     self.obstacle_function(obstacle_coords, '#36b38b')

        elif self.chosen_envi == envi_options[3]:
            
            # obstacle envi 2
            # Obstacle Wall co ordinates for the maze
            obstacle_coords = [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0], [10,0]]
            # render obstacle block using dynamic function
            self.obstacle_function(obstacle_coords, '#000000')


        # Creating an agent of Mobile Robot - red point
        self.agent = self.create_object(self.agentLocation, fill_color = 'red')
        # self.agent = self.canvas_widget.create_oval(
        #     self.o[0] - 14, self.o[1] - 14,
        #     self.o[0] + 14, self.o[1] + 14,
        #     outline='#FF1493', fill='#FF1493')

        # Final Point
        '''img_flag = Image.open("images/flag.png")
        self.flag_object = ImageTk.PhotoImage(img_flag)
        self.flag = self.canvas_widget.create_image(pixels * 11, pixels * 5, anchor='nw', image=self.flag_object)'''

        # Final Point - yellow point
        if self.chosen_envi == envi_options[0] or self.chosen_envi == envi_options[1]: # 'Obstacle':
            flag_center = self.o + np.array([pixels * 8, pixels * 4])
        elif self.chosen_envi == envi_options[3]: #'Cliff Walk':
            flag_center = self.o + np.array([pixels * 11, 0])
        else:
            flag_center = self.o + np.array(self.flagLocation)
        # Building the flag
        self.flag = self.canvas_widget.create_rectangle(
            flag_center[0] - 20, flag_center[1] - 20,  # Top left corner
            flag_center[0] + 20, flag_center[1] + 20,  # Bottom right corner
            outline='grey', fill='yellow')
        # Saving the coordinates of the final point according to the size of agent
        # In order to fit the coordinates of the agent
        self.coords_flag = [self.canvas_widget.coords(self.flag)[0] + 6,
                            self.canvas_widget.coords(self.flag)[1] + 6,
                            self.canvas_widget.coords(self.flag)[2] - 6,
                            self.canvas_widget.coords(self.flag)[3] - 6]

        # Uploading the image of Mobile Robot
        #img_robot = Image.open("images/agent1.png")
        #self.robot = ImageTk.PhotoImage(img_robot)
        # Creating an agent with photo of Mobile Robot
        #self.agent = self.canvas_widget.create_image(0, pixels*5, anchor='nw', image=self.robot)
        

        # Packing everything
        self.canvas_widget.pack()
    

    def reset(self):
        self.update()

        # reset the agent at initial position
        self.canvas_widget.delete(self.agent)
        self.agent = self.create_object(self.agentLocation, fill_color = 'red')
        #self.agent = self.canvas_widget.create_image(0, pixels*5, anchor='nw', image=self.robot)
        # self.agent = self.canvas_widget.create_oval(
        #     self.o[0] - 14, self.o[1] - 14,
        #     self.o[0] + 14, self.o[1] + 14,
        #     outline='red', fill='red')
        # reset the dictionary and the i
        
        self.d = {}
        self.i = 0

        # Return initial state of an agent
        return self.canvas_widget.coords(self.agent)


     # Function to get the next observation and reward by doing next step

    def step(self, action):
        # Current state of the agent
        state = self.canvas_widget.coords(self.agent) 
            # state = [4,5] // [col, row]
            # e.g. state[0] = 4 | state[1] = 5 
        base_action = np.array([0, 0])

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[1] >= pixels:
                base_action[1] -= pixels
        # Action 'down'
        elif action == 1:
            if state[1] < (self.env_height - 1) * pixels:
                base_action[1] += pixels
        # Action right
        elif action == 2:
            if state[0] < (self.env_width - 1) * pixels:
                base_action[0] += pixels
        # Action left
        elif action == 3:
            if state[0] >= pixels:
                base_action[0] -= pixels

        # Moving the agent according to the action
        self.canvas_widget.move(self.agent, base_action[0], base_action[1])

        # Writing in the dictionary coordinates of found route
        self.d[self.i] = self.canvas_widget.coords(self.agent)

        # Updating next state
        next_state = self.d[self.i]
        
        # Updating key for the dictionary
        self.i += 1

        # Calculating the reward for the agent
        #if next_state == self.canvas_widget.coords(self.flag):
        if next_state == self.coords_flag:
        
            if(self.chosen_envi == envi_options[3]): # cliff walk
                reward = 10
            else:
                reward = 1
            done = True
            next_state = 'goal'

            # Filling the dictionary first time
            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest:
                self.longest = len(self.d)

        # check if user has chosen obstacle environment, then update reward
        elif self.chosen_envi in envi_options and next_state in self.obstacle_walls:
            if(self.chosen_envi == envi_options[3]): # cliff walk
                reward = -100
            else:
                reward = -1

            done = True
            next_state = 'obstacle'
            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0
        else:
            if(self.chosen_envi == envi_options[3]): # cliff walk
                reward = -1
            else:
                reward = 0
            done = False
        return next_state, reward, done


    # Function to refresh the environment
    def render(self):
        #time.sleep(0.03)
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        #print('The shortest route:', self.shortest)
        #print('The longest route:', self.longest)

        # Creating initial point
        
        # origin = np.array([20, 20])
        # self.initial_point = self.canvas_widget.create_oval(
        #     self.o[0] - 5, self.o[1] - 5,
        #     self.o[0] + 5, self.o[1] + 5,
        #     fill='blue', outline='blue')
        if self.chosen_envi == envi_options[0] or self.chosen_envi == envi_options[1]: # 'Obstacle':
            origin = np.array([20, 180])
        else:
            origin = np.array([20, 20])
        self.initial_point = self.canvas_widget.create_oval(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='blue', outline='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            ## print(self.f[j])
            self.track = self.canvas_widget.create_oval(
                self.f[j][0] - 4 + origin[0] - 5, self.f[j][1] - 4 + origin[0] - 5,
                self.f[j][0] - 4 + origin[0] + 5, self.f[j][1] - 4 + origin[0] + 5,
                fill='blue', outline='blue')
            # Writing the final route in the global variable a
            a[j] = self.f[j] 

        return self.shortest, self.longest                

    def clearFoundPath(self):
        time.sleep(1)
        #self.canvas_widget.delete(self.track)

    # function to create and add agent in maze 
    def create_object(self, obstacle_coords, fill_color = 'red'): 
        obstacle_var = self.o + np.array([pixels* obstacle_coords[0], pixels * obstacle_coords[1]])
        
        # Building the agent
        return self.canvas_widget.create_oval(
            obstacle_var[0] - 14, obstacle_var[1] - 14,  # Top left corner
            obstacle_var[0] + 14, obstacle_var[1] + 14,  # Bottom right corner
            outline='red', fill= fill_color)

    # function to create obstacle in the maze          
    def obstacle_function(self, obstacle_coords, fill_color = '#00BFFF'):
        
        for i in range(len(obstacle_coords)):
                
            obstacle_var = self.o + np.array([pixels* obstacle_coords[i][0], pixels * obstacle_coords[i][1]])
            
            # Building the obstacle
            obstacle = self.canvas_widget.create_rectangle(
                obstacle_var[0] - 20, obstacle_var[1] - 20,  # Top left corner
                obstacle_var[0] + 20, obstacle_var[1] + 20,  # Bottom right corner
                outline='grey', fill= fill_color)
            # Saving the coordinates of obstacle 1 according to the size of agent
            # In order to fit the coordinates of the agent
            obstacle_coord_item = [self.canvas_widget.coords(obstacle)[0] + 6,
                self.canvas_widget.coords(obstacle)[1] + 6,
                self.canvas_widget.coords(obstacle)[2] - 6,
                self.canvas_widget.coords(obstacle)[3] - 6]
            self.obstacle_walls += [obstacle_coord_item]
        
# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a



# to run and view the environment for testing
if __name__ == '__main__':
    env = Environment()
    env.mainloop()