"""
Article storage manager
Handles saving and loading news.json
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime


PROJECT_FOLDER = Path(__file__).parent.parent

ARTICLE_FOLDER = PROJECT_FOLDER / "articles"

DATABASE_FILE = PROJECT_FOLDER / "news.json"


ARTICLE_FOLDER.mkdir(exist_ok=True)



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

    article_id = create_id(url)

    filename = article_id + ".html"

    filepath = ARTICLE_FOLDER / filename


    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            article["html"]
        )


    # Path used by the website
    web_path = (
        "articles/" + filename
    )


    return {

        "id": article_id,

        "title": article["title"],

        "url": url,

        "file": web_path,

        "downloaded": datetime.now().isoformat(),

        "read": False,

        "saved": False

    }
