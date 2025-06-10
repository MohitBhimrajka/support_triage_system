import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=None)
def load_agent_configs() -> dict:
    """
    Loads agent configurations from the agents.yaml file.
    The result is cached to avoid repeated file I/O.
    """
    config_path = Path(__file__).parent / "agents.yaml"
    print(f"Loading agent configurations from: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)