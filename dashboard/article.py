from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup


from dashboard.utils import clean_filename


PROJECT_ROOT = Path(__file__).parent.parent


# Maximum time to wait for an individual article.
# Separate connect/read timeouts prevent a server from
# keeping the workflow hanging indefinitely.
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 20


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": (
        "en-CA,en-US;q=0.9,en;q=0.8"
    ),
    "Accept-Encoding": (
        "gzip, deflate"
    ),
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def download_article(article):

    """
    Download and save one article.

    Returns a dictionary containing:

        status:
            saved
            blocked
            missing
            error

        file:
            relative article path when saved

        message:
            explanation when unsuccessful
    """


    # --------------------------------------------------
    # Get article information
    # --------------------------------------------------

    url = (
        article.get("url")
        or article.get("link")
    )


    if not url:

        return {
            "status": "error",
            "message": "No URL found",
            "file": None
        }


    source = article.get(
        "source",
        "unknown"
    )


    title = article.get(
        "title",
        "untitled"
    )


    # --------------------------------------------------
    # Create article folder
    # --------------------------------------------------

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


    # --------------------------------------------------
    # Create filename
    # --------------------------------------------------

    article_id = article.get(
        "id",
        ""
    )


    if article_id:

        article_id = article_id[:8]


    filename = (
        clean_filename(title)
        + "-"
        + article_id
        + ".html"
    )


    filepath = folder / filename


    # --------------------------------------------------
    # Download article
    # --------------------------------------------------

    print(
        f"  Downloading: {title}"
    )


    print(
        f"  URL: {url}"
    )


    try:

        response = requests.get(

            url,

            timeout=(
                CONNECT_TIMEOUT,
                READ_TIMEOUT
            ),

            headers=HEADERS,

            allow_redirects=True

        )


    except requests.exceptions.Timeout:

        print(
            "  TIMEOUT:",
            url
        )


        return {
            "status": "error",
            "message": "Request timed out",
            "file": None
        }


    except requests.exceptions.ConnectionError as e:

        print(
            "  CONNECTION ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": "Connection error",
            "file": None
        }


    except requests.exceptions.RequestException as e:

        print(
            "  REQUEST ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": str(e),
            "file": None
        }


    except Exception as e:

        print(
            "  UNEXPECTED ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": str(e),
            "file": None
        }


    # --------------------------------------------------
    # Check HTTP status
    # --------------------------------------------------

    status_code = response.status_code


    print(
        f"  HTTP status: {status_code}"
    )


    if status_code == 403:

        print(
            "  BLOCKED (403):",
            source
        )


        return {
            "status": "blocked",
            "message": "HTTP 403",
            "file": None
        }


    if status_code == 404:

        print(
            "  NOT FOUND (404):",
            url
        )


        return {
            "status": "missing",
            "message": "HTTP 404",
            "file": None
        }


    if status_code == 429:

        print(
            "  RATE LIMITED (429):",
            source
        )


        return {
            "status": "blocked",
            "message": "HTTP 429",
            "file": None
        }


    if status_code >= 500:

        print(
            f"  SERVER ERROR ({status_code}):",
            source
        )


        return {
            "status": "error",
            "message": f"HTTP {status_code}",
            "file": None
        }


    try:

        response.raise_for_status()


    except requests.exceptions.RequestException as e:

        print(
            "  HTTP ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": str(e),
            "file": None
        }


    # --------------------------------------------------
    # Parse HTML
    # --------------------------------------------------

    try:

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


    except Exception as e:

        print(
            "  HTML PARSE ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": "HTML parsing failed",
            "file": None
        }


    # --------------------------------------------------
    # Remove unnecessary page elements
    # --------------------------------------------------

    for tag in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]
    ):

        tag.decompose()


    # --------------------------------------------------
    # Make sure there is actually content
    # --------------------------------------------------

    text = soup.get_text(
        " ",
        strip=True
    )


    if len(text) < 200:

        print(
            "  WARNING: Very little page content"
        )


        return {
            "status": "error",
            "message": "Page contained very little readable content",
            "file": None
        }


    # --------------------------------------------------
    # Save article
    # --------------------------------------------------

    try:

        filepath.write_text(
            str(soup),
            encoding="utf-8"
        )


    except OSError as e:

        print(
            "  FILE SAVE ERROR:",
            str(e)
        )


        return {
            "status": "error",
            "message": str(e),
            "file": None
        }


    # --------------------------------------------------
    # Return website-relative path
    # --------------------------------------------------

    relative_path = filepath.relative_to(
        PROJECT_ROOT
    )


    relative_path = str(
        relative_path
    ).replace(
        "\\",
        "/"
    )


    print(
        "  SAVED:",
        relative_path
    )


    return {
        "status": "saved",
        "file": relative_path
    }
