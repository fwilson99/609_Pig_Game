from value_iteration import ValueIteration, AsynchValueIteration, load_mdp_from_csv, MDP

# Define state space
S = [(0, 0, 0),
     (1, 0, 0),
     (0, 1, 0),
     (1, 1, 0),
     (0, 0, 1),
     (0, 1, 1),
     (1, 0, 1),
     (1, 1, 1),
     (0, 0, 2),
     (0, 1, 2)]

# Define which actions ("hold" and "roll") can occur at each state
A = {}

for s in S[:-4]:
    A.update({s: ["hold", "roll"]})

# Define the transition probabilities. The key is in the form (current state, action, next state).
P = {}

for s in S[:-4]:
    P.update({(s, "hold", (s[0] + s[2], s[1], 0)): 1})
    P.update({(s, "roll", (s[0], s[1], s[2] + 1)): 0.5})
    P.update({(s, "roll", (s[0], s[1], 0)): 0.5})

# Define the reward function. The key is in the form (current state, action, next state).
# For this example the reward is only dependent on the current state and the action.
# Therefore, there are duplicates.
# Sometimes the reward is also dependent on the next state and so we need to define it in this way.
R = {
    ((0, 0, 1), "roll", (0, 0, 2)): 1,
    ((1, 0, 0), "roll", (1, 0, 1)): 1,
    ((0, 1, 1), "roll", (0, 1, 2)): 1,
    ((1, 1, 0), "roll", (1, 1, 1)): 1,
}

# Create MDP data class
mdp = MDP(states=S, actions=A, probabilities=P, rewards=R)

# Setup value iteration class (synchronous version)
value_itr = ValueIteration(mdp=mdp, gamma=1, theta=1e-6, printing=True)

# Run value iteration algorithm
optimal_values, optimal_policy = value_itr.value_iteration()

# Display results
print("Optimal State Values:", optimal_values)
print("Optimal Policy:", optimal_policy)