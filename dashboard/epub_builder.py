"""
Personal Newspaper EPUB Builder

Creates an EPUB newspaper from the articles
stored in news.json and the articles folder.
"""

import json
from pathlib import Path
from datetime import datetime

from ebooklib import epub


PROJECT_FOLDER = Path(__file__).parent.parent

DATABASE_FILE = PROJECT_FOLDER / "news.json"

EXPORT_FOLDER = PROJECT_FOLDER / "exports"



def load_database():
    """Load the article database."""

    if not DATABASE_FILE.exists():

        print("news.json not found")

        return {
            "articles": []
        }


    with open(
        DATABASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def get_article_html(article):
    """Load an article HTML file."""

    file_path = PROJECT_FOLDER / article["file"]


    if not file_path.exists():

        print(
            "Missing article:",
            article["title"]
        )

        return None


    try:

        return file_path.read_text(
            encoding="utf-8"
        )


    except Exception as error:

        print(
            "Could not read:",
            article["title"]
        )

        print(error)

        return None



def clean_html(html):
    """
    Basic cleanup for EPUB.

    Removes document-level tags so article
    content can be placed inside EPUB chapters.
    """

    html = html.replace(
        "<!DOCTYPE html>",
        ""
    )

    html = html.replace(
        "<html>",
        ""
    )

    html = html.replace(
        "</html>",
        ""
    )

    html = html.replace(
        "<body>",
        ""
    )

    html = html.replace(
        "</body>",
        ""
    )

    return html



def create_front_page(book, article_count):

    today = datetime.now().strftime(
        "%B %d, %Y"
    )


    front_page = epub.EpubHtml(
        title="Personal Newspaper",
        file_name="front-page.xhtml",
        lang="en"
    )


    front_page.content = f"""
    <html>
    <head>
        <title>Personal Newspaper</title>
    </head>

    <body>

        <h1>Personal Newspaper</h1>

        <h2>{today}</h2>

        <p>
            {article_count} articles
        </p>

        <p>
            Your personal offline news edition.
        </p>

    </body>
    </html>
    """


    book.add_item(
        front_page
    )


    return front_page



def build_epub():

    database = load_database()

    articles = database.get(
        "articles",
        []
    )


    if not articles:

        print(
            "No articles found"
        )

        return



    print()
    print(
        "Building Personal Newspaper"
    )
    print(
        "Articles:",
        len(articles)
    )
    print()



    EXPORT_FOLDER.mkdir(
        exist_ok=True
    )


    book = epub.EpubBook()



    # Metadata

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    book.set_identifier(
        f"personal-newspaper-{today}"
    )


    book.set_title(
        f"Personal Newspaper - {today}"
    )


    book.set_language(
        "en"
    )


    book.add_author(
        "Personal Dashboard"
    )



    # CSS

    style = """

    body {
        font-family: serif;
        line-height: 1.6;
    }

    h1 {
        margin-top: 1em;
    }

    h2 {
        margin-top: 1.5em;
    }

    p {
        margin-bottom: 1em;
    }

    """



    css = epub.EpubItem(
        uid="style",
        file_name="style/newspaper.css",
        media_type="text/css",
        content=style
    )


    book.add_item(
        css
    )



    # Front page

    front_page = create_front_page(
        book,
        len(articles)
    )



    chapters = []



    for number, article in enumerate(
        articles,
        start=1
    ):


        print(
            f"[{number}/{len(articles)}]",
            article["title"]
        )


        html = get_article_html(
            article
        )


        if html is None:

            continue



        html = clean_html(
            html
        )



        article_id = article.get(
            "id",
            str(number)
        )



        chapter = epub.EpubHtml(
            title=article["title"],
            file_name=(
                f"articles/{article_id}.xhtml"
            ),
            lang="en"
        )



        source = article.get(
            "source",
            ""
        )


        category = article.get(
            "category",
            ""
        )


        chapter.content = f"""

        <html>

        <head>

            <link
                rel="stylesheet"
                type="text/css"
                href="../style/newspaper.css"
            />

        </head>


        <body>


            <h1>
                {article["title"]}
            </h1>


            <p>

                <strong>
                    {source}
                </strong>

                {category}

            </p>


            <hr />


            {html}


        </body>

        </html>

        """



        book.add_item(
            chapter
        )


        chapters.append(
            chapter
        )



    # Table of contents

    # Table of contents

book.toc = [
    front_page,
    *chapters
]



    # Reading order

    book.spine = [

        "nav",

        front_page,

        *chapters

    ]



    # Navigation

    book.add_item(
        epub.EpubNcx()
    )


    book.add_item(
        epub.EpubNav()
    )



    # Write file

    output_file = (
        EXPORT_FOLDER /
        f"Personal-Newspaper-{today}.epub"
    )


    epub.write_epub(
        str(output_file),
        book,
        {}
    )



    print()
    print(
        "EPUB created:"
    )

    print(
        output_file
    )


    print()
    print(
        "Articles included:",
        len(chapters)
    )



if __name__ == "__main__":

    build_epub()
