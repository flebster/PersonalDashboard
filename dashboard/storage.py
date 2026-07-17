"""
Article storage manager
Handles saving articles and news.json
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime


PROJECT_FOLDER = Path(__file__).parent.parent

ARTICLE_FOLDER = PROJECT_FOLDER / "articles"

DATABASE_FILE = PROJECT_FOLDER / "news.json"


def load_database():

    if not DATABASE_FILE.exists():

        return {
            "articles": []
        }

    with open(
        DATABASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_database(database):

    print("Saving database:", DATABASE_FILE)

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


def create_id(url):

    return hashlib.sha1(
        url.encode("utf-8")
    ).hexdigest()


def article_exists(database, url):

    article_id = create_id(url)

    for article in database["articles"]:

        if article["id"] == article_id:

            return True

    return False


def save_article(article, url):

    print("Creating article folder:", ARTICLE_FOLDER)

    ARTICLE_FOLDER.mkdir(
        exist_ok=True
    )

    article_id = create_id(url)

    filename = article_id + ".html"

    filepath = ARTICLE_FOLDER / filename


    print("Saving article:", filepath)


    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            article["html"]
        )


    print("Saved:", filepath)


    return {

        "id": article_id,

        "title": article["title"],

        "url": url,

        "file": str(filepath),

        "downloaded": datetime.now().isoformat(),

        "read": False,

        "saved": False

    }
