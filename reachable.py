import random

from optimal_policy import extract_optimal_policy
from pig_game import PigGame, PigPlayer
from utilities import load_value_function, store_value_function

#for plotting test
import matplotlib.pyplot as plt
import numpy as np

# Load raw value function from JSON
filename = "data/value_function/pig/goal_100.json"
V = load_value_function(filename)

# Extract optimal policy
optimal_policy = extract_optimal_policy(V=V, goal=100)

reachable = {(0, 30, 0): 1} # define this initial state as reachable

#initialise
goal = 100 #set goal
j = 30 #set opponent score for cross section

for i in range(goal):
    for k in range(goal):
        #see if a state is reachable
        try:
            if reachable[(i, j, k)] == 1 and optimal_policy[(i, j, k)] == "roll":
                #from 2,3,4,5,6 to add reachability
                for x in range(2,7):
                    if i + k + x < 100:
                        reachable[(i, j, k + x)] = 1
            
            elif reachable[(i, j, k)] == 1 and optimal_policy[(i, j, k)] == "hold":
                if i + k < 100:
                    reachable[(i + k, j, 0)] = 1

        #KeyError likely to exist if state is not reachable, then
        except KeyError:
            reachable[(i, j, k)] = 0

store_reachable = True
filename = f"data/reachable/pig/goal_{goal}_opponent_score_{j}.json"

if store_reachable:
    store_value_function(filename=filename, V=reachable)

reachable = load_value_function(filename)

#plotting test done as heatmap
# Create a 2D array to hold reachability values
reachable_matrix = np.zeros((100, 100))  # rows = k, cols = i

# Fill the matrix based on the reachable dict
for i in range(100):
    for k in range(100):
        reachable_matrix[k, i] = reachable.get((i, j, k), 0)

# Plot heatmap using matplotlib
plt.figure(figsize=(10, 8))
plt.imshow(reachable_matrix, origin='lower', cmap='Blues', aspect='auto')

plt.xlabel("i (player score)")
plt.ylabel("k (turn total)")
plt.title(f"Reachable States with Opponent Score j = {j}")
plt.xticks(np.arange(0, 100, 10))
plt.yticks(np.arange(0, 100, 10))

plt.show()