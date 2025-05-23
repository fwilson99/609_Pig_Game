"""Module providing the value iteration routine applied to the Piglet game. Results are optionally stored to prevent rerunning the code many times."""

from utilities import store_value_function, store_value_tracker

goal = 2

# Non-terminal states
states = []
for i in range(goal):
    for j in range(goal):
        for k in range(goal - i):
            states.append((i, j, k))

# Initialise value function
V = {s: 0 for s in states}

# Initialise convergence parameter
epsilon = 1e-6

# For tracking values at each iteration
value_tracker = [[] for _ in range(len(states))]

while True:

    delta = 0
    new_V = {}

    x = 0  # a counter

    for s in states:
        i, j, k = s

        # The player can hold and win
        if i + k >= goal:
            new_V[s] = 1

        # If not a win
        else:
            # Roll: 0.5 chance to get a tail (turn passes), 0.5 chance to increment k
            # If a tail: (i, j, k) -> (j, i, 0) - remove turn points (k=0) and swap i and j (ending turn)
            # If a head: (i, j, k) -> (i, j, k + 1) - add a turn point (k += 1)
            if i + k + 1 >= goal:
                roll_val = 0.5 * ((1 - V[(j, i, 0)]) + 1)
            else:
                roll_val = 0.5 * ((1 - V[(j, i, 0)]) + V[(i, j, k + 1)])

            # Hold: turn passes with i+k added to score
            if i + k >= goal:
                hold_val = 1
            else:
                # (i, j, k) -> (j, i + k, 0)
                # First bank the points and reset turn total: (i, j, k) -> (i + k, j, 0)
                # Since "hold" action was taken, switch players: (j, i + k, 0)
                hold_val = 1 - V[(j, i + k, 0)]

            new_V[s] = max(roll_val, hold_val)

            delta = max(delta, abs(new_V[s] - V[s]))

        # Add this iteration's value function to the tracker
        value_tracker[x].append(new_V[s])

        x += 1

    V = new_V

    if delta < epsilon:
        break

# Store value function and value tracker for future use
store_win_probabilities = True
filename = f"data/value_function/piglet/goal_{goal}.json"
tracker_filename = f"data/value_function/piglet/value_tracker_goal_{goal}.json"

if store_win_probabilities:
    store_value_function(filename=filename, V=V)
    store_value_tracker(tracker_filename, value_tracker)
