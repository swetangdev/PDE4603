# list of environments, first three as used for the analysis
# envi_options = ['Obstacle', 'Obstacle Pipe', 'In-Path Obstacle','Obstacle Cross', 'Obstacle Walls', 'Cliff Walk']
envi_options = ['Obstacle', 'Obstacle Pipe', 'In-Path Obstacle', 'Cliff Walk']
class user_choice_class:
    def __init__(self):
        self.user_input = 1
        self.check_user_input()
        
    #show user input screen to select appropriate choice
    def check_user_input(self):
        while True:
            try:
                self.user_input = self.get_user_input()
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue
            
            if self.user_input > len(envi_options) or self.user_input < 0:
                print("Sorry, please choose between 0 and 4.")
                continue
            elif self.user_input == 0:
                exit()
            else:
                break
        
    # ask user for choose an enviornment
    def get_user_input(self):
        print('Please enter your choice for environment')
        
        print('0 Exit')
        for env_item in range(len(envi_options)):
            print((env_item+1),envi_options[env_item])
            
        choose_envi = int(input('Please enter your choice:'))
        return choose_envi

    
    # get environment based on user choice
    def get_selected_envi(self):
        return envi_options[self.user_input-1]

   
