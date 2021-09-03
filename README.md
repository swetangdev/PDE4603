# PDE4603 Thesis - Analysis on Q-Learning and SARSA algorithm

## Description
* Analysis Script is created that run algorithm miltiple time.
* Analysis done using the script that perform iterations on certain combinations of (gamma, epsilon) parameters rather than just FIXED gamma, epsilon values.
  ```
  gamma_array = [0.7, 0.6]
  epsilon_array = [0.6, 0.5, 0.4]
  ```
  * So, as per above values it will run algorithm 2x3 = 6 times
 * At the end of execution of script, it will create analysis.csv file with information like ... Route (short, long, time) and Q-Table (Full, Final)
 using this analysis file we can study that for which combination it gives better result in terms of  e.g. shortest path and lower execution time.
 And further will select different set of array based on best found combination to perform another execution and so on.
 
 #### This will help to find best possible parameters (gamma and epsilon) but it "might" depends on the type of environment.
