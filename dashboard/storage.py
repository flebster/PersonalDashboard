"""
Stores downloaded articles.
"""

import hashlib

from pathlib import Path


PROJECT_FOLDER = Path(__file__).parent.parent

ARTICLE_FOLDER = PROJECT_FOLDER / "articles"

ARTICLE_FOLDER.mkdir(exist_ok=True)


def article_filename(url):

    return hashlib.sha1(

        url.encode("utf-8")

    ).hexdigest() + ".html"


def save_article(article, url):

    filename = article_filename(url)

    path = ARTICLE_FOLDER / filename

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(article["html"])

    return filename
