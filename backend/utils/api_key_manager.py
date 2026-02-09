import os
from itertools import cycle
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / "key.env"

load_dotenv(dotenv_path=ENV_PATH)

_key_cycles = {}

def get_next_key(env_var_name: str) -> str:
    if env_var_name not in _key_cycles:
        keys = os.getenv(env_var_name)

        if not keys:
            raise Exception(f"No API keys found for {env_var_name}")

        key_list = [k.strip() for k in keys.split(",") if k.strip()]
        _key_cycles[env_var_name] = cycle(key_list)

    return next(_key_cycles[env_var_name])
