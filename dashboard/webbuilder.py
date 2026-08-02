"""
Builds the web dashboard files.

Copies the article database into the web folder
so GitHub Pages can display the dashboard.
"""

from pathlib import Path
import shutil


PROJECT_FOLDER = Path(__file__).parent.parent

WEB_FOLDER = PROJECT_FOLDER / "web"

NEWS_FILE = PROJECT_FOLDER / "news.json"



def build_web_dashboard():

    print("Preparing web dashboard")


    # Make sure web folder exists

    WEB_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


    if not NEWS_FILE.exists():

        print(
            "news.json not found"
        )

        return



    # Copy database to website

    destination = (
        WEB_FOLDER /
        "news.json"
    )


    shutil.copy2(
        NEWS_FILE,
        destination
    )


    print(
        "Copied news.json to web folder"
    )


    print(
        destination
    )
