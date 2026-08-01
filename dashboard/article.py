from pathlib import Path
from datetime import datetime
import requests

from bs4 import BeautifulSoup

from dashboard.utils import clean_filename


PROJECT_ROOT = Path(__file__).parent.parent


def download_article(article):

    url = article.get("url") or article.get("link")

    source = article.get(
        "source",
        "unknown"
    )


    today = datetime.utcnow()


    folder = (
        PROJECT_ROOT
        / "articles"
        / str(today.year)
        / f"{today.month:02d}"
        / clean_filename(source)
    )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        clean_filename(article["title"])
        + ".html"
    )


    filepath = folder / filename


    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )


        if response.status_code == 403:

            return {
                "status": "blocked",
                "file": None
            }


        if response.status_code == 404:

            return {
                "status": "missing",
                "file": None
            }


        response.raise_for_status()


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer"
            ]
        ):
            tag.decompose()


        filepath.write_text(
            str(soup),
            encoding="utf-8"
        )


        relative = filepath.relative_to(
            PROJECT_ROOT
        )


        return {
            "status": "saved",
            "file": str(relative)
        }


    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
            "file": None
        }
