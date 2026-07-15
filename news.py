"""
Personal Dashboard
Main program
"""

from dashboard.config import load_config
from dashboard.feeds import load_feeds
from dashboard.downloader import get_articles
from dashboard.article import download_article
from dashboard.storage import save_article


def main():

    # Load configuration
    config = load_config()

    # Load RSS feeds
    feeds = load_feeds()

    print()
    print("=" * 70)
    print(config["application"]["name"])
    print("=" * 70)
    print()

    total_feeds = 0
    total_articles = 0
    downloaded_articles = 0

    for feed in feeds:

        total_feeds += 1

        print(f"Checking {feed['name']}...")

        try:

            articles = get_articles(feed)

        except Exception as error:

            print(f"Error reading feed: {error}")
            print()
            continue

        print(f"Found {len(articles)} articles")

        total_articles += len(articles)

        #
        # Only download the first 3 articles while testing.
        # Later we'll remove this limit.
        #
        for article in articles[:3]:

            print(f"  Downloading: {article['title']}")

            downloaded = download_article(article["link"])

            if downloaded is None:

                print("    Failed.")
                continue

            filename = save_article(
                downloaded,
                article["link"]
            )

            downloaded_articles += 1

            print(f"    Saved as {filename}")

        print()

    print("=" * 70)
    print("Finished")
    print("=" * 70)

    print(f"Feeds checked      : {total_feeds}")
    print(f"Articles found     : {total_articles}")
    print(f"Articles saved     : {downloaded_articles}")

    print("=" * 70)


if __name__ == "__main__":
    main()
