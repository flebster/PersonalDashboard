import json
from pathlib import Path
from datetime import datetime
import shutil


PROJECT_ROOT = Path(__file__).parent

NEWS_FILE = PROJECT_ROOT / "news.json"

BACKUP_FILE = (
    PROJECT_ROOT /
    f"news_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
)


OLD_PATH = (
    "/home/runner/work/"
    "PersonalDashboard/"
    "PersonalDashboard/"
)


NEW_PATH = "articles/"


def main():

    print("Starting news.json migration")


    if not NEWS_FILE.exists():

        print("news.json not found")

        return


    # Backup original file

    shutil.copy(
        NEWS_FILE,
        BACKUP_FILE
    )


    print(
        "Backup created:",
        BACKUP_FILE.name
    )


    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        database = json.load(f)


    changed = 0


    for article in database.get(
        "articles",
        []
    ):


        old_file = article.get(
            "file"
        )


        if old_file and OLD_PATH in old_file:


            article["file"] = (
                old_file
                .replace(
                    OLD_PATH,
                    ""
                )
                .replace(
                    "\\",
                    "/"
                )
            )


            changed += 1



    with open(
        NEWS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            database,
            f,
            indent=2,
            ensure_ascii=False
        )


    print()
    print("==============================")
    print("Migration Complete")
    print("==============================")

    print(
        "Articles updated:",
        changed
    )

    print(
        "Total articles:",
        len(
            database.get(
                "articles",
                []
            )
        )
    )

    print("==============================")


if __name__ == "__main__":

    main()
