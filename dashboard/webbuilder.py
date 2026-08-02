"""
Builds the GitHub Pages website files.

GitHub Pages can deploy from:
- repository root
- /docs

This builder publishes the dashboard files
to the repository root.
"""

from pathlib import Path
import shutil


PROJECT_FOLDER = Path(__file__).parent.parent

NEWS_FILE = PROJECT_FOLDER / "news.json"

WEB_FOLDER = PROJECT_FOLDER / "web"



def copy_file(source, destination):

    if source.exists():

        shutil.copy2(
            source,
            destination
        )

        print(
            "Copied:",
            source.name,
            "->",
            destination.name
        )

    else:

        print(
            "Missing:",
            source
        )



def build_web_dashboard():

    print()
    print("Preparing GitHub Pages dashboard")
    print("-------------------------------")


    # Copy data file

    copy_file(
        NEWS_FILE,
        PROJECT_FOLDER / "news.json"
    )


    # Copy frontend files from web folder

    frontend_files = [
        "index.html",
        "style.css",
        "app.js"
    ]


    for filename in frontend_files:

        copy_file(
            WEB_FOLDER / filename,
            PROJECT_FOLDER / filename
        )


    print("-------------------------------")
    print("Dashboard build complete")
    print()



if __name__ == "__main__":

    build_web_dashboard()
