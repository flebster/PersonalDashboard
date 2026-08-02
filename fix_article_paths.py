"""
Fix old GitHub Actions runner paths
in news.json.

Converts:

/home/runner/work/PersonalDashboard/PersonalDashboard/articles/file.html

to:

articles/file.html
"""

import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).parent

DATABASE_FILE = PROJECT_FOLDER / "news.json"


def main():

    print("Fixing article paths...")


    with open(
        DATABASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        database = json.load(file)



    changed = 0


    for article in database["articles"]:

        old_path = article.get(
            "file",
            ""
        )


        if "articles/" in old_path:

            filename = old_path.split(
                "articles/"
            )[-1]


            new_path = (
                "articles/" +
                filename
            )


            if old_path != new_path:

                article["file"] = new_path

                changed += 1



    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            database,
            file,
            indent=2,
            ensure_ascii=False
        )


    print(
        "Updated paths:",
        changed
    )


if __name__ == "__main__":

    main()
