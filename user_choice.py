def get_user_input():
    print('Please enter your choice for environment')
    print('0. Exit')
    print('1. No Obstacle')
    print('2. One Obstacle')
    
    choose_envi = int(input('Please enter your choice:'))
    return choose_envi

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