# The MAZE environment

import numpy as np  # for data manipulation in matrix form
import tkinter as tk # for making GUI
import time # for time calculation
from PIL import Image, ImageTk
from numpy.core.records import array

# define the size of an environment, 12 x 12 maze with each of 20 pixels
pixels = 40
env_height = 12
env_width = 12
total_env_height = env_height * pixels
total_env_width = env_width * pixels


# Global variable for dictionary with coordinates for the final route
a = {}
environment_name = ''

# class for environment 

class Environment(tk.Tk, object):
    def __init__(self, field):
        super(Environment, self).__init__()
        self.actions = ['up','down','left','right']

        # using ternary condition check if Algo, Envi options are exist or set it default value
        field['algo'] = 'R-Learning' if 'algo' not in field else field['algo']
        field['envi'] = 'no-obstcle' if 'envi' not in field else field['envi']
        
        print('Chosen Evnironment: ', field['envi'])
        
        self.title(field['algo'] + ' - Environment')
        
        # set chosen environment
        self.chosen_envi = field['envi']

        self.total_actions = len(self.actions)
        self.geometry('{0}x{1}'.format(total_env_height, total_env_width))
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
        self.canvas_widget = tk.Canvas(self,  bg='white', height = total_env_height, width= total_env_width)

        # Creating grid lines
        for column in range(0, env_width * pixels, pixels):
            x0, y0, x1, y1 = column, 0, column, env_height * pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, env_height * pixels, pixels):
            x0, y0, x1, y1 = 0, row, env_height * pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

        # check if user has chosen obstacle environment, then add obstacle to environment
        if self.chosen_envi == 'Obstacle':
            img_obstacle1 = Image.open("images/square.png")
            self.obstacle1_object = ImageTk.PhotoImage(img_obstacle1)
            self.obstacle1 = self.canvas_widget.create_image(pixels * 5, pixels * 5, anchor='nw', image=self.obstacle1_object)

        # Final Point
        img_flag = Image.open("images/flag.png")
        self.flag_object = ImageTk.PhotoImage(img_flag)
        self.flag = self.canvas_widget.create_image(pixels * 11, pixels * 5, anchor='nw', image=self.flag_object)

        # Uploading the image of Mobile Robot
        img_robot = Image.open("images/agent1.png")
        self.robot = ImageTk.PhotoImage(img_robot)
        # Creating an agent with photo of Mobile Robot
        self.agent = self.canvas_widget.create_image(0, pixels*5, anchor='nw', image=self.robot)

        # Packing everything
        self.canvas_widget.pack()


    def reset(self):
        self.update()

        # reset the agent at initial position
        self.canvas_widget.delete(self.agent)
        self.agent = self.canvas_widget.create_image(0, pixels*5, anchor='nw', image=self.robot)

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
            if state[1] < (env_height - 1) * pixels:
                base_action[1] += pixels
        # Action right
        elif action == 2:
            if state[0] < (env_width - 1) * pixels:
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
        if next_state == self.canvas_widget.coords(self.flag):
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

        # check if user has chosen obstacle environment, then add obstacle to environment
        
        elif self.chosen_envi == 'Obstacle' and next_state in [self.canvas_widget.coords(self.obstacle1)]:
            reward = -1
            done = True
            next_state = 'obstacle'
        
            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0

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
        origin = np.array([20, 220])
        self.initial_point = self.canvas_widget.create_oval(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='blue', outline='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            ## print(self.f[j])
            self.track = self.canvas_widget.create_oval(
                self.f[j][0] + origin[0] - 5, self.f[j][1] + origin[0] - 5,
                self.f[j][0] + origin[0] + 5, self.f[j][1] + origin[0] + 5,
                fill='blue', outline='blue')
            # Writing the final route in the global variable a
            a[j] = self.f[j] 

        return self.shortest, self.longest                

    def clearFoundPath(self):
        time.sleep(1)
        #self.canvas_widget.delete(self.track)

# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a



# to run and view the environment for testing
if __name__ == '__main__':
    env = Environment()
    env.mainloop()