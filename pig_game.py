"""Module defining classes for the pig game mechanics, and pig players with different strategies."""

import math
import random


class PigPlayer:
    """Player class for the game Pig."""

    def __init__(
        self,
        name: str,
        target: int | float = 50,
        dice_sides: int = 6,
        strategy: str = "rolls",
        number_dice: int = 1,
        policy=None,
    ):
        """Initialise a pig player.

        Args:
            name (str): The name of the player.
            target (int | float, optional): The target which to reach to determine a winner.
                                            Defaults to 50.
            dice_sides (int, optional): The number of sides of the dice. Defaults to 6.
            strategy (str, optional): The strategy to determine whether to play on or not.
            number_dice (int, optional): Number of dice to roll each turn. Defaults to 1.
            policy (optional): Optimal Pig play policy. Defaults to None.

        Raises:
            ValueError: Strategy is not a valid value.
            TypeError: Dice sides is non-integer.
            TypeError: Number of dice is non-integer.
        """
        # Raise all possible errors
        if strategy not in ["rolls", "cumulativeScore", "holdAt20", "optimal"]:
            raise ValueError(
                "Invalid strategy - must be one of rolls, cumulativeScore, holdAt20, optimal"
            )
        if not isinstance(dice_sides, int):
            raise TypeError("Only integers are allowed for the number of dice sides.")
        if not isinstance(number_dice, int):
            raise TypeError("Only integers are allowed for the number of dice.")

        # If passed error validation, set class variables.
        self.strategy = strategy
        self.number_dice = number_dice
        self.dice_sides = dice_sides
        self.name = name
        self.target = target
        self.failure_roll = 1  # Jeopardy dice roll
        # Score trackers
        self.cumulative_score = 0
        self.round_score = 0
        self.round_rolls = 0
        # Strategy specific variables
        self.prob_fail = 1 - (1 - 1 / self.dice_sides) ** self.number_dice
        self.expected_rolls_to_fail = math.floor(1 / self.prob_fail)
        self.expected_avg_roll = (
            number_dice * sum(range(1, dice_sides + 1)) / dice_sides
        )
        self.policy = policy

    def roll(self) -> int | list[int]:
        """Simulate dice roll(s) and return the value of the roll(s).

        Returns:
            int | list[int]: Dice roll, or multiple dice rolls if there are multiple dice.
        """
        if self.number_dice == 1:
            return random.randint(1, self.dice_sides)
        return [random.randint(1, self.dice_sides) for _ in range(self.number_dice)]

    def reset_round(self) -> None:
        """Reset the round to score 0 and number of rolls 0."""
        self.round_score = 0
        self.round_rolls = 0

    def end_round(self) -> None:
        """End the round based on player's strategy (i.e. cumulative score increases)."""
        self.cumulative_score += self.round_score
        self.reset_round()

    def determine_failure(self, roll_value: int | list[int]) -> bool:
        """Determine whether the roll was jeopardy causing failure.

        Additionally, reset round on failure or increment round statistics.

        Args:
            roll_value (int | list[int]): Value of the player's dice roll(s).

        Returns:
            bool: Whether to end the round or not.
        """
        # If the player rolls the jeopardy value, fail
        failure = False
        if self.number_dice > 1:
            if any(roll == self.failure_roll for roll in roll_value):
                failure = True
        else:
            if roll_value == self.failure_roll:
                failure = True

        if failure:
            self.reset_round()
            return True

        # Increase number of rolls and round score
        self.round_rolls += 1
        self.increment_round_score(roll_value=roll_value)
        return False

    def increment_round_score(self, roll_value: int | list[int]) -> None:
        """Increment the round's score after a successful round depending on the number of die.

        Args:
            roll_value (int | list[int]): The dice roll(s).
        """
        if self.number_dice > 1:
            self.round_score += sum(roll_value)
        else:
            self.round_score += roll_value

    def action(self) -> bool:
        """Determine if the player should play another round or not based on their strategy.

        Raises:
            ValueError: If the chosen strategy is optimal, a policy must be provided.
            NotImplementedError: If strategy provided is invalid.

        Returns:
            bool: Return True if the player should play another round, otherwise False.
        """
        if self.strategy == "rolls":
            if self.round_rolls == self.expected_rolls_to_fail - 1:
                self.end_round()
                return False
            return True

        elif self.strategy == "cumulativeScore":
            if self.round_score >= self.expected_avg_roll * (
                self.expected_rolls_to_fail - 1
            ):
                self.end_round()
                return False
            return True

        elif self.strategy == "holdAt20":
            if self.round_score >= 20:
                self.end_round()
                return False
            return True

        elif self.strategy == "optimal":
            if self.policy is None:
                raise ValueError("Policy must be provided for optimal strategy.")

            # Extract the opponent's score (the opponent with highest score)
            opponent_score = max(p.cumulative_score for p in self.opponents)

            # Extract optimal action for the state
            state = (self.cumulative_score, opponent_score, self.round_score)
            action = self.policy.get(state, "hold")  # "hold" is default action

            if action == "hold":
                self.end_round()
                return False
            return True

        else:
            raise NotImplementedError("Strategy not implemented!")


class PigGame:
    """Class simulating the pig game dynamics given a list of players."""

    def __init__(
        self, players: list[PigPlayer], target: int = 50, print_terminal: bool = True
    ):
        """Set up the pig game.

        Args:
            players (list[PigPlayer]): List of pig players - the order determines the round order.
            target (int, optional): Target of cumulative rolls at which to end game. Defaults to 50.
            print_terminal (bool, optional): Whether to print output to terminal. Defaults to True.
        """
        self.players = players
        self.target = target
        self.game_round = 1
        self.print_terminal = print_terminal

    def get_winner(self) -> PigPlayer:
        """Return the player who won the game.

        Returns:
            PigPlayer: Winner of pig game.
        """
        return max(self.players, key=lambda p: p.cumulative_score)

    def announce_winner(self) -> None:
        """Compute and print winner with their score."""
        game_winner = self.get_winner()
        print(
            f"\nThe winner is {game_winner.name} with a score of {game_winner.cumulative_score}!"
        )

    def simulate(self) -> None:
        """Simulate the pig game."""
        game_over = False
        while not game_over:
            if self.print_terminal:
                print(f"\nRound {self.game_round}")
            for i, player in enumerate(self.players):
                # Opponents scores are required for players with optimal policy
                player.opponents = self.players[:i] + self.players[i + 1 :]
                while True:
                    roll = player.roll()
                    # Determine whether to end round due to fail
                    if player.determine_failure(roll):
                        break
                    # Determine whether to end round due to strategy
                    if not player.action():
                        break

                if player.cumulative_score >= self.target:
                    if self.print_terminal:
                        print(f"{player.name} has reached the target score!")
                    game_over = True
                    break

            self.game_round += 1
            if self.print_terminal:
                for player in self.players:
                    print(f"{player.name}: {player.cumulative_score}")

        # Announce winner
        if self.print_terminal:
            self.announce_winner()
