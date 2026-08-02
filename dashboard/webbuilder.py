"""
Builds the GitHub Pages website files.

GitHub Pages deploys from repository root.
This copies frontend files from /web to the root.
"""

from pathlib import Path
import shutil


PROJECT_FOLDER = Path(__file__).parent.parent

WEB_FOLDER = PROJECT_FOLDER / "web"



def copy_file(source, destination):

    if not source.exists():

        print(
            "Missing:",
            source
        )

        return


    if source.resolve() == destination.resolve():

        print(
            "Already in place:",
            destination.name
        )

        return


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



def build_web_dashboard():

    print()
    print("Preparing GitHub Pages dashboard")
    print("-------------------------------")


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
