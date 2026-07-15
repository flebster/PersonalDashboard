"""
Downloads a webpage and extracts the readable article.
"""

import requests

from readability import Document

from bs4 import BeautifulSoup


def download_article(url):

    try:

        response = requests.get(
            url,
            timeout=20
        )

        response.raise_for_status()

    except Exception as error:

        print("Failed:", url)

        print(error)

        return None

    document = Document(response.text)

    title = document.short_title()

    html = document.summary()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return {

        "title": title,

        "html": html,

        "text": text

    }
