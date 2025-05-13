"""Module performing a competition between pig players (optimal policy vs hold at 20)."""

import random

from optimal_policy import extract_optimal_policy
from pig_game import PigGame, PigPlayer
from utilities import load_value_function


# Load raw value function from JSON
filename = "data/value_function/pig/goal_100.json"
V = load_value_function(filename)

# Extract optimal policy
optimal_policy = extract_optimal_policy(V=V, goal=100)

# Initialise competition variables
random.seed(12345)
target = 100
rounds = 1000

# --- Test optimal policy against itself ---
# Determine what proportion of times the starting player wins
opt_vs_opt_starter_wins = 0

for _ in range(rounds):
    players = [
        PigPlayer(
            name="player_1", target=target, strategy="optimal", policy=optimal_policy
        ),
        PigPlayer(
            name="player_2", target=target, strategy="optimal", policy=optimal_policy
        ),
    ]
    game = PigGame(players=players, target=target, print_terminal=False)
    game.simulate()
    winner = game.get_winner()
    if winner.name == "player_1":
        opt_vs_opt_starter_wins += 1

print(
    f"Optimal vs Optimal: Starting player win rate: {100*opt_vs_opt_starter_wins / rounds}%"
)

# --- Test optimal policy against Hold At 20 player ---
# Determine what proportion of times the holdAt20 player wins when starting
holdAt20_starter_wins = 0

for _ in range(rounds):
    players = [
        PigPlayer(name="player_1", target=target, strategy="holdAt20"),
        PigPlayer(
            name="player_2", target=target, strategy="optimal", policy=optimal_policy
        ),
    ]
    game = PigGame(players=players, target=target, print_terminal=False)
    game.simulate()
    winner = game.get_winner()
    if winner.name == "player_1":
        holdAt20_starter_wins += 1

print(
    f"Hold at 20 vs Optimal: Starting player (Hold at 20) win rate: {100*holdAt20_starter_wins / rounds}%"
)

# Determine what proportion of times the optimal player wins when starting
opt_starter_wins = 0

for _ in range(rounds):
    players = [
        PigPlayer(
            name="player_1", target=target, strategy="optimal", policy=optimal_policy
        ),
        PigPlayer(name="player_2", target=target, strategy="holdAt20"),
    ]
    game = PigGame(players=players, target=target, print_terminal=False)
    game.simulate()
    winner = game.get_winner()
    if winner.name == "player_1":
        opt_starter_wins += 1

print(
    f"Hold at 20 vs Optimal: Starting player (Optimal) win rate: {100*opt_starter_wins / rounds}%"
)
