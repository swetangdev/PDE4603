# PDE4603 Thesis - Comparison analysis of Reinforcement Learning Algorithms (Q-learning and SARSA) for global path planning

- The model-free reinforcement learning algorithms, Q-Learning and SARSA do not need the knowledge of the environment. In Q-learning, Q means Quality, the main goal is to guide an agent to learn quality actions and help agent to decide what action to be taken in a scenario. SARSA is different than Q-learning, in which it does not focus on maximum reward for next state rather it continues to follow same policy for every transition. In this section, four different environments are used for the comparison of Q-Learning and SARSA algorithms with the number of experimental trials.
- The environments used here are from single obstacle in single path, vertically stacked obstacles in the single path, obstacle in the individual possible paths and cliff-walking environment. There are 1000 episodes run for each experiment.
- The performance of the learning algorithms is decided based on a different combination of parameters that produces assort results. The ideal algorithm should provide the shortest path to the goal in less time and the same learning rate regardless of the complexity of the environment. The standard parameters discount factor, epsilon, and learning rate played an important role to check and tune the performance of both algorithms in each environment and checked which parameters range are providing expected results.

## Software Requirement: 
- Python Prerequisites: https://cs205uiuc.github.io/guidebook/resources/python-prerequisites.html
  - Download and setup Jupyter Notebook: https://jupyter.org/
  - Download and setup Anaconda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html
  - Check whether python successfully installed on system by running command to check python version, in command window ``` python -V ```
## Following python libraries may required to run script:
  library dependency installation

```sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install python3-tk 
sudo apt-get remove python3-pil python3-pil.imagetk python-pil.imagetk python-pil
sudo apt-get install python3-pil.imagetk # Note that python3-pil installed as a dependency
pip install Pillow
sudo apt install python3-pandas
```

## Run following commands to execute algorithm
  - for Q-Learning ```python .\execute_Q_agent.py```
  - for SARSA ```python .\execute_SARSA_agent.py```

Above command it will show following :

<img src="https://user-images.githubusercontent.com/46344128/138363740-2bebaaad-a8e9-4f0a-a10b-18105ce0ecc6.png" width="600" />


After selecting environment it will start executing experiment trials (10 trials) for each combination of supplied array of Gamma and Epsilon: 


<img src="https://user-images.githubusercontent.com/46344128/138364059-557a2bdf-f470-413c-88a6-a3eabe955603.png" width="600" />

At the end of execution it will generate two CSV files: 
 - For example: 
    - SARSA_analysis_{envi_name}_{date-time}.csv
      - <img src="https://user-images.githubusercontent.com/46344128/138365579-8ab25bf5-d2c9-4e87-850f-a7b8317dec88.png" width="600" height="600" />
    - SARSA_analysis-AVG_{envi_name}_{date-time}.csv
      - <img src="https://user-images.githubusercontent.com/46344128/138365725-cca1de7c-db82-4904-aa92-d773d84ad0c5.png" width="300" />



----------------------------------

## Script Description
* Analysis Script is created that run algorithm miltiple time.
* Analysis done using the script that perform iterations on certain combinations of (gamma, epsilon) parameters rather than just FIXED gamma, epsilon values.
  ```
  gamma_array = [0.7, 0.6]
  epsilon_array = [0.6, 0.5, 0.4]
  ```
  * So, as per above values it will run algorithm 2x3 = 6 times
 
 * Execution code do following tasks:
    - The script iterating on each gamma value from the array with all epsilon values from the collection. For every gamma-epsilon pair, it will perform 10 trials. For example, three gamma values, three epsilon values, and 10 trials, then it will do ten trials for each gamma-epsilon combination (3x3x10 = 90 trials total)
    - During every iteration, it initiates the Q-Table and runs a learning algorithm with several episodes, and returns information including shortest/longest path, length of Q-table, and total time taken and all this information is stored in auto-generated CSV files that are used for further analysis.
    - In addition to this, the maze script (is responsible for generating grid environment, choosing the next step, deciding final route, handling obstacles, etc) is modified to render the chosen environment with the agent's initial location, destination location, and final path.


## Following types of environments used for this projects: 
Environment 1: Single Obstacle

![image](https://user-images.githubusercontent.com/46344128/138361912-73b1b4f3-a21d-4f80-930b-ebc04a51a516.png)
![image](https://user-images.githubusercontent.com/46344128/138362015-1b809938-9e66-4d5e-bfeb-7508645753f3.png)


Environment 1: Pipe-Shape Obstacle

![image](https://user-images.githubusercontent.com/46344128/138362027-29dc6fef-f8e1-4dd3-bfd2-9c5518748a93.png)
![image](https://user-images.githubusercontent.com/46344128/138361919-dce82cc4-ff74-452e-b14f-ffd474e9651b.png)

Environment 3: In-path Obastacle

![image](https://user-images.githubusercontent.com/46344128/138361928-ec4bc6af-5b68-45fd-981e-ef0c7aed66ae.png)
![image](https://user-images.githubusercontent.com/46344128/138362040-fb8df7a0-c790-4c6f-9111-866834cb5e85.png)


Environment 4: Cliff Walking

![image](https://user-images.githubusercontent.com/46344128/138361943-19f8dc95-bc2a-4388-870d-cfb296566039.png)
![image](https://user-images.githubusercontent.com/46344128/138361944-d2d74195-5c92-4dea-a559-b60f25fe864f.png)

 
 
 


## Final Result Summary:


<img src="https://user-images.githubusercontent.com/46344128/138361774-34ecd519-d5b7-4e29-a92e-2d0c4fef8233.png" width="600" />
