"""
Creates files needed by the web dashboard.
"""

import shutil
from pathlib import Path


PROJECT_FOLDER = Path(__file__).parent.parent

SOURCE = PROJECT_FOLDER / "news.json"

WEB_FOLDER = PROJECT_FOLDER / "web"

DESTINATION = WEB_FOLDER / "news.json"


def build_web_dashboard():

    WEB_FOLDER.mkdir(
        exist_ok=True
    )

    shutil.copy(
        SOURCE,
        DESTINATION
    )

    print(
        "Web dashboard updated:"
    )

    print(
        DESTINATION
    )
