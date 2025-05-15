"""Module with utility/ helper functions for storing and loading data, as well as running Pig competitions between optimal players and players following the hold at 20 strategy."""

import json
import os
import math
import random
from scipy.stats import norm

from pig_game import PigGame, PigPlayer


def store_value_tracker(filename: str, value_tracker: list[list[float]]):
    """Store the value tracker as JSON.

    Args:
        filename (str): Filename to store the value tracker as.
        value_tracker (list[list[float]]): Value tracker object.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        json.dump(value_tracker, f)


def load_value_tracker(filename: str) -> list[list[float]]:
    """Load the value tracker from a JSON file.

    Args:
        filename (str): Filename where the JSON is stored.

    Returns:
        list[list[float]]: Value tracker object.
    """
    with open(filename, "r") as f:
        value_tracker = json.load(f)
    return value_tracker


def store_value_function(filename: str, V: dict[tuple[int, int, int], float]):
    """Store the value function for pig or piglet as a JSON.

    Args:
        filename (str): Filename to store the file as.
        V (dict[tuple[int, int, int], float]): Value function.
    """
    # Convert tuple keys to strings (JSON doesn't accept tuple keys)
    string_V = {str(key): value for key, value in V.items()}

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Store JSON file
    with open(filename, "w") as f:
        json.dump(string_V, f)


def load_value_function(filename: str) -> dict[tuple[int, int, int], float]:
    """Load the value function from JSON as a dictionary.

    Args:
        filename (str): Filename of the stored JSON.

    Returns:
        dict[tuple[int, int, int], float]: Value function.
    """
    with open(filename, "r") as f:
        raw_V = json.load(f)

    # Convert string keys to tuples (JSON doesn't accept tuple keys)
    V = {eval(k): v for k, v in raw_V.items()}

    return V


def compute_confidence_interval(
    wins: int, trials: int, confidence: float = 0.95
) -> tuple[float, float, float]:
    """Compute the confidence interval for a probability (i.e. Wald interval).

    Get the binomial proportion confidence interval for a given confidence.

    Args:
        wins (int): Number of wins.
        trials (int): Number of trials.
        confidence (float, optional): Confidence level required. Defaults to 0.95.

    Returns:
        tuple[float, float, float]: mean proportion, lower confidence bound, upper confidence bound.
    """
    # Get probability estimate
    p = wins / trials
    # Get z-score for the confidence level
    z = norm.ppf(1 - (1 - confidence) / 2)
    # Compute standard error
    se = math.sqrt(p * (1 - p) / trials)
    return (p, p - z * se, p + z * se)


def competition(
    player_1_strategy: str,
    player_2_strategy: str,
    optimal_policy: None | dict[tuple[int, int, int], float] = None,
    target: int = 100,
    rounds: int = 1000,
) -> tuple[float, float, float]:
    """Run the Pig competition and return the proportion of starter player wins with a 95% confidence interval.

    Args:
        player_1_strategy (str): Player 1 strategy - should be "optimal" or "holdAt20".
        player_2_strategy (str): Player 2 strategy - should be "optimal" or "holdAt20".
        optimal_policy (None | dict[tuple[int, int, int], float], optional): Optimal Pig game policy. Defaults to None.
        target (int, optional): Goal of the game to win. Defaults to 100.
        rounds (int, optional): Number of simulations to run. Defaults to 1000.

    Returns:
        tuple[float, float, float]: mean proportion, lower confidence bound, upper confidence bound.
    """
    # Count the numner
    player_1_starter_wins = 0

    for _ in range(rounds):
        players = [
            PigPlayer(
                name="player_1",
                target=target,
                strategy=player_1_strategy,
                policy=optimal_policy if player_1_strategy == "optimal" else None,
            ),
            PigPlayer(
                name="player_2",
                target=target,
                strategy=player_2_strategy,
                policy=optimal_policy if player_2_strategy == "optimal" else None,
            ),
        ]
        game = PigGame(players=players, target=target, print_terminal=False)
        game.simulate()
        winner = game.get_winner()
        if winner.name == "player_1":
            player_1_starter_wins += 1

    p, CI_lower, CI_upper = compute_confidence_interval(
        wins=player_1_starter_wins, trials=rounds
    )

    return p, CI_lower, CI_upper


def competition_random_start(
    optimal_policy: dict[tuple[int, int, int], float],
    target: int = 100,
    rounds: int = 1000,
) -> tuple[float, float, float]:
    """Simulates games where one player is optimal and one is holdAt20, with random starting positions.

    Goal: Determine the proportion of times the optimal player wins when starting position is randomised (vs hold at 20).

    Args:
        optimal_policy (dict[tuple[int, int, int], float]): Optimal Pig game policy.
        target (int, optional): Goal of the game to win. Defaults to 100.
        rounds (int, optional): Number of simulations to run. Defaults to 1000.

    Returns:
        tuple[float, float, float]: mean proportion, lower confidence bound, upper confidence bound.
    """
    optimal_wins = 0

    for _ in range(rounds):
        if random.random() < 0.5:
            # Optimal goes first
            players = [
                PigPlayer(
                    name="player_1",
                    target=target,
                    strategy="optimal",
                    policy=optimal_policy,
                ),
                PigPlayer(name="player_2", target=target, strategy="holdAt20"),
            ]
        else:
            # Optimal goes second
            players = [
                PigPlayer(name="player_1", target=target, strategy="holdAt20"),
                PigPlayer(
                    name="player_2",
                    target=target,
                    strategy="optimal",
                    policy=optimal_policy,
                ),
            ]

        game = PigGame(players=players, target=target, print_terminal=False)
        game.simulate()
        winner = game.get_winner()
        if winner.strategy == "optimal":
            optimal_wins += 1

    p, CI_lower, CI_upper = compute_confidence_interval(optimal_wins, rounds)
    return p, CI_lower, CI_upper
