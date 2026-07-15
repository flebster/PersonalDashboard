from dashboard.config import load_config
from dashboard.feeds import load_feeds
from dashboard.downloader import get_articles


def main():

    config = load_config()

    feeds = load_feeds()

    print()
    print("=" * 60)
    print(config["application"]["name"])
    print("=" * 60)

    total_articles = 0

    for feed in feeds:

        articles = get_articles(feed)

        total_articles += len(articles)

        for article in articles[:5]:

            print(f"   • {article['title']}")

        print()

    print("=" * 60)
    print(f"Finished. {total_articles} total articles found.")
    print("=" * 60)


if __name__ == "__main__":
    main()
