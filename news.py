from dashboard.config import load_config
from dashboard.feeds import load_feeds


def main():

    config = load_config()

    feeds = load_feeds()

    print()

    print(config["application"]["name"])

    print()

    print("Feeds loaded:")

    print()

    for feed in feeds:

    print(f"Name:      {feed['name']}")
    print(f"Category:  {feed['category']}")
    print(f"RSS Feed:  {feed['url']}")
    print("-" * 60)

if __name__ == "__main__":

    main()
