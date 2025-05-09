"""Module proving code to extract the optimal policy for a pig game given a value function."""


def extract_optimal_policy(
    V: dict[tuple[int, int, int], float],
    goal: int = 100,
    dice_sides: int = 6,
) -> dict[tuple[int, int, int], float]:
    """Given a value function, determine the optimal policy for the game of Pig.

    Args:
        V (dict[tuple[int, int, int], float]): Value function for all states.
            - States are the form (current player's score, opponent's score, turn total).
        goal (int, optional): The number of points required to win. Defaults to 100.
        dice_sides (int, optional): Number of dice sides. Defaults to 6.

    Returns:
        dict[tuple[int, int, int], float]: Optimal action policy per state.
    """
    # Extract states
    states = list(V.keys())

    # Policy storage
    policy = {}

    for s in states:
        i, j, k = s

        # Already won - hold position.
        if i + k >= goal:
            policy[s] = "hold"
            continue

        # Compute value of action "roll"
        if i + k + dice_sides >= goal:
            r_star = goal - i - k

            if r_star <= 2:
                num_winning_rolls = dice_sides - 1
                roll_val = (1 / dice_sides) * ((1 - V[(j, i, 0)]) + num_winning_rolls)
            else:
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

        # Compute value of action "hold"
        hold_val = 1 - V[(j, i + k, 0)]

        # Determine optimal action
        if roll_val > hold_val:
            policy[s] = "roll"
        else:
            policy[s] = "hold"

    return policy
