"""
Article downloader and extractor
"""

import requests

from readability import Document

from bs4 import BeautifulSoup


def download_article(url):

    print("Downloading:", url)

    try:

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()


    except Exception as error:

        print("Download failed:")
        print(error)

        return None


    try:

        document = Document(
            response.text
        )

        html = document.summary()

        title = document.short_title()


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


    except Exception as error:

        print("Extraction failed:")
        print(error)

        return None
