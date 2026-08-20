"""
Personal Newspaper EPUB Builder

Creates an EPUB newspaper from the articles
stored in news.json and the articles folder.
"""

import json
from pathlib import Path
from datetime import datetime
from html import escape

from ebooklib import epub


PROJECT_FOLDER = Path(__file__).parent.parent

DATABASE_FILE = PROJECT_FOLDER / "news.json"

EXPORT_FOLDER = PROJECT_FOLDER / "exports"


def load_database():
    """Load the article database."""

    if not DATABASE_FILE.exists():
        print("news.json not found")
        return {"articles": []}

    with open(
        DATABASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def get_article_html(article):
    """Load an article HTML file."""

    article_file = article.get("file")

    if not article_file:
        print(
            "Missing file reference:",
            article.get("title", "Untitled")
        )
        return None

    file_path = PROJECT_FOLDER / article_file

    if not file_path.exists():
        print(
            "Missing article:",
            article.get("title", "Untitled")
        )
        print("Expected:", file_path)
        return None

    try:
        return file_path.read_text(
            encoding="utf-8"
        )

    except Exception as error:
        print(
            "Could not read:",
            article.get("title", "Untitled")
        )
        print(error)
        return None


def clean_html(html):
    """Remove document-level HTML tags."""

    replacements = [
        "<!DOCTYPE html>",
        "<!doctype html>",
        "<html>",
        "</html>",
        "<body>",
        "</body>",
        "<head>",
        "</head>",
    ]

    for tag in replacements:
        html = html.replace(tag, "")

    return html


def create_front_page(book, article_count, date_string):
    """Create the newspaper front page."""

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

        <h2>{escape(date_string)}</h2>

        <p>
            {article_count} articles
        </p>

        <p>
            Personal Dashboard offline edition.
        </p>

        <hr>

        <p>
            Use the table of contents to browse the articles.
        </p>

    </body>
    </html>
    """

    book.add_item(front_page)

    return front_page


def build_epub():

    database = load_database()

    articles = database.get(
        "articles",
        []
    )

    if not articles:
        print("No articles found")
        return

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    display_date = datetime.now().strftime(
        "%B %d, %Y"
    )

    print()
    print("------------------------------")
    print("Building Personal Newspaper")
    print("------------------------------")
    print("Articles:", len(articles))
    print()

    EXPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    book = epub.EpubBook()

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

    book.set_identifier(
        f"personal-newspaper-{today}"
    )

    book.set_title(
        f"Personal Newspaper - {today}"
    )

    book.set_language("en")

    book.add_author(
        "Personal Dashboard"
    )

    # -------------------------------------------------
    # CSS
    # -------------------------------------------------

    style = """
    body {
        font-family: serif;
        font-size: 1.1em;
        line-height: 1.6;
        margin-left: 5%;
        margin-right: 5%;
    }

    h1 {
        font-size: 1.7em;
        line-height: 1.2;
        margin-top: 1em;
    }

    h2 {
        font-size: 1.4em;
    }

    p {
        margin-bottom: 1em;
    }

    img {
        max-width: 100%;
        height: auto;
    }

    hr {
        margin-top: 1.5em;
        margin-bottom: 1.5em;
    }
    """

    css = epub.EpubItem(
        uid="newspaper_css",
        file_name="style/newspaper.css",
        media_type="text/css",
        content=style
    )

    book.add_item(css)

    # -------------------------------------------------
    # Front page
    # -------------------------------------------------

    front_page = create_front_page(
        book,
        len(articles),
        display_date
    )

    chapters = []

    # -------------------------------------------------
    # Articles
    # -------------------------------------------------

    for number, article in enumerate(
        articles,
        start=1
    ):

        title = article.get(
            "title",
            "Untitled Article"
        )

        print(
            f"[{number}/{len(articles)}] {title}"
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

        source = article.get(
            "source",
            ""
        )

        category = article.get(
            "category",
            ""
        )

        published = article.get(
            "published",
            ""
        )

        metadata = ""

        if source:
            metadata += (
                f"<strong>{escape(source)}</strong>"
            )

        if category:
            metadata += (
                f" &nbsp; {escape(category)}"
            )

        if published:
            metadata += (
                f" &nbsp; {escape(str(published))}"
            )

        chapter = epub.EpubHtml(
            title=title,
            file_name=(
                f"articles/{article_id}.xhtml"
            ),
            lang="en"
        )

        chapter.content = f"""
        <html>

        <head>
            <title>{escape(title)}</title>

            <link
                rel="stylesheet"
                type="text/css"
                href="../style/newspaper.css"
            />
        </head>

        <body>

            <h1>{escape(title)}</h1>

            <p>
                {metadata}
            </p>

            <hr>

            {html}

        </body>

        </html>
        """

        chapter.add_item(css)

        book.add_item(
            chapter
        )

        chapters.append(
            chapter
        )

    # -------------------------------------------------
    # Table of contents
    # -------------------------------------------------

    book.toc = [
        front_page,
        *chapters
    ]

    # -------------------------------------------------
    # Navigation
    # -------------------------------------------------

    book.add_item(
        epub.EpubNcx()
    )

    book.add_item(
        epub.EpubNav()
    )

    # -------------------------------------------------
    # Reading order
    # -------------------------------------------------

    book.spine = [
        "nav",
        front_page,
        *chapters
    ]

    # -------------------------------------------------
    # Create EPUB
    # -------------------------------------------------

    output_file = (
        EXPORT_FOLDER
        / f"Personal-Newspaper-{today}.epub"
    )

    epub.write_epub(
        str(output_file),
        book
    )

    print()
    print("------------------------------")
    print("EPUB created successfully")
    print("------------------------------")
    print(output_file)
    print()
    print(
        "Articles included:",
        len(chapters)
    )


if __name__ == "__main__":
    build_epub()
