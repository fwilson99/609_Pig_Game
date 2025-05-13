import json
import os


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
