"""Module computing the reachablity of each of the states under the optimal policy for the game Pig."""

from optimal_policy import extract_optimal_policy
from utilities import load_value_function, store_value_function

# Load raw value function from JSON
filename = "data/value_function/pig/goal_100.json"
V = load_value_function(filename)

# Extract optimal policy
optimal_policy = extract_optimal_policy(V=V, goal=100)

reachable = {(0, 30, 0): 1}  # define this initial state as reachable

# initialise
goal = 100  # set goal
j = 30  # set opponent score for cross section

for i in range(goal):
    for k in range(goal):
        # see if a state is reachable
        try:
            if reachable[(i, j, k)] == 1 and optimal_policy[(i, j, k)] == "roll":
                # from 2,3,4,5,6 to add reachability
                for x in range(2, 7):
                    if i + k + x < 100:
                        reachable[(i, j, k + x)] = 1

            elif reachable[(i, j, k)] == 1 and optimal_policy[(i, j, k)] == "hold":
                if i + k < 100:
                    reachable[(i + k, j, 0)] = 1

        # KeyError likely to exist if state is not reachable, then
        except KeyError:
            reachable[(i, j, k)] = 0

store_reachable = True
filename = f"data/reachable/pig/goal_{goal}_opponent_score_{j}.json"

if store_reachable:
    store_value_function(filename=filename, V=reachable)
