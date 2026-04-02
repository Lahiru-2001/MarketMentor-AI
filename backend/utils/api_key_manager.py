import os
from itertools import cycle  # To create an infinite cycle iterator over API keys
from dotenv import load_dotenv  # To load environment variables from a .env file
from pathlib import Path  # To handle file paths in an OS-independent way


# Get the base directory of the project (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parents[1]

# Define the path to the environment file containing API keys
ENV_PATH = BASE_DIR / "key.env"

# Load environment variables from the specified file
load_dotenv(dotenv_path=ENV_PATH)

# Dictionary to store cycle iterators for different environment variables
_key_cycles = {}


def get_next_key(env_var_name: str) -> str:
    """
    Retrieve the next API key from a comma-separated list of keys in environment variables.
    Uses a cycle iterator to rotate through keys infinitely.
    
    Parameters:
        env_var_name (str): Name of the environment variable containing the API keys.
        
    Returns:
        str: The next API key in rotation.
        
    Raises:
        Exception: If no keys are found for the given environment variable.
    """
    
    # If this environment variable hasn't been used before, initialize a cycle iterator
    if env_var_name not in _key_cycles:
        # Get the comma-separated keys from environment variables
        keys = os.getenv(env_var_name)

        # Raise an exception if no keys are found
        if not keys:
            raise Exception(f"No API keys found for {env_var_name}")

        # Split keys by comma, strip whitespace, and create a cycle iterator
        key_list = [k.strip() for k in keys.split(",") if k.strip()]
        _key_cycles[env_var_name] = cycle(key_list)

    # Return the next key in the cycle
    return next(_key_cycles[env_var_name])