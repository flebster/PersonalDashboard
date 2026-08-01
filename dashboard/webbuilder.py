"""
Creates files needed by the web dashboard.
"""

from pathlib import Path
import shutil


PROJECT_FOLDER = Path(__file__).parent.parent

SOURCE = PROJECT_FOLDER / "news.json"


def build_web_dashboard():

    print("Preparing web dashboard")

    if not SOURCE.exists():
        print("news.json not found")
        return


    print("Dashboard data already available:")
    print(SOURCE)
