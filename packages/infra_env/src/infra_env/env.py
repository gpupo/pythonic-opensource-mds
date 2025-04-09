import os
from pathlib import Path

from dotenv import load_dotenv

MAX_LEVEL_RECURSION = 5


def load_env(level: int = 1, recursive: bool = True, filename: str = ".env") -> bool:
    """
    Load a .env file from a specified number of directory levels above the current file.

    Args:
        level (int): Number of directory levels to go up (default: 1).
        recursive (bool): If True, searches upwards up to the specified level.
                          If False, only checks the exact level.
        filename (str): The name of the .env file (default: ".env").

    Returns:
        bool: True if a .env file was successfully loaded, False otherwise.
    """
    base_path = Path(__file__).resolve().parent

    levels = range(1, level + MAX_LEVEL_RECURSION) if recursive else [level]
    for i in levels:
        env_file = base_path.parents[i - 1] / filename
        if env_file.is_file():
            load_dotenv(env_file)
            return True

    return False


def is_running_in_container() -> bool:
    """
    Detect whether the current environment is a Docker or Kubernetes container.

    Returns:
        bool: True if running inside a container, False otherwise.
    """
    return os.path.exists("/.dockerenv") or "KUBERNETES_SERVICE_HOST" in os.environ
