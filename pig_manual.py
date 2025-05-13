import json
import os

goal = 100
dice_sides = 6

# Non-terminal states
states = []
for i in range(goal):
    for j in range(goal):
        for k in range(goal - i):
            states.append((i, j, k))

# Initialise value function
V = {s: 0 for s in states}
V_roll = {s: 0 for s in states}
V_hold = {s: 0 for s in states}

# Initialise convergence parameter
epsilon = 1e-6

# Progress Tracker
progress = 1

while True:
    print(f"Iteration {progress}")

    delta = 0
    new_V = {}
    new_V_roll = {}
    new_V_hold = {}

    for s in states:
        i, j, k = s

        # The player can hold and win
        if i + k >= goal:
            new_V[s] = 1
            new_V_roll[s] = 0
            new_V_hold[s] = 1

        # If not a win
        else:

            if i + k + dice_sides >= goal:
                # Smallest r that wins (i + k + r >= goal)
                r_star = goal - i - k

                if r_star <= 2:
                    # All non-1 rolls are wins (roll = {1, 2})
                    num_winning_rolls = dice_sides - 1
                    roll_val = (1 / dice_sides) * (
                        (1 - V[(j, i, 0)]) + num_winning_rolls
                    )

                else:
                    # Some rolls are non-terminal, others are wins
                    roll_val = (1 / dice_sides) * (
                        (1 - V[(j, i, 0)])
                        + sum(V[(i, j, k + r)] for r in range(2, r_star))
                        + (dice_sides - r_star + 1)
                    )
            else:
                roll_val = (1 / dice_sides) * (
                    (1 - V[(j, i, 0)])
                    + sum(V[(i, j, k + r)] for r in range(2, dice_sides + 1))
                )

            # Hold: turn passes with i+k added to score
            if i + k >= goal:
                hold_val = 1
            else:
                # (i, j, k) -> (j, i + k, 0)
                # First bank the points and reset turn total: (i, j, k) -> (i + k, j, 0)
                # Since "hold" action was taken, switch players: (j, i + k, 0)
                hold_val = 1 - V[(j, i + k, 0)]

            new_V[s] = max(roll_val, hold_val)
            new_V_roll[s] = roll_val
            new_V_hold[s] = hold_val

            delta = max(delta, abs(new_V[s] - V[s]))

    V = new_V
    V_roll = new_V_roll
    V_hold = new_V_hold

    if delta < epsilon:
        break

    progress += 1

# Store value function for future use
store_win_probabilities = True
filename = f"data/value_function/goal_{goal}.json"

if store_win_probabilities:
    # Convert tuple keys to strings (JSON doesn't accept tuple keys)
    string_V = {str(key): value for key, value in V.items()}

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Store JSON file
    with open(filename, "w") as f:
        json.dump(string_V, f)

print("Win probabilities:", V)
print(min(V.values()))
print(max(V.values()))

