"""
Reads feeds.txt
"""

from pathlib import Path


PROJECT_FOLDER = Path(__file__).parent.parent

FEEDS_FILE = PROJECT_FOLDER / "feeds.txt"


def load_feeds():

    feeds = []

    with FEEDS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            if line.startswith("#"):
                continue

            parts = line.split("|")

            if len(parts) != 3:

                print(
                    "Skipping bad feed:",
                    line
                )

                continue

            feeds.append({

                "name": parts[0],

                "url": parts[1],

                "category": parts[2]

            })

    return feeds
