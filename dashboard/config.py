"""
Configuration loader

Reads config.json and provides project settings.
"""

import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).parent.parent

CONFIG_FILE = PROJECT_FOLDER / "config.json"


def load_config():

    with CONFIG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
