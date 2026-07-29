from dashboard.config import load_config
from dashboard.feeds import load_feeds
from dashboard.downloader import get_articles
from dashboard.article import download_article
from dashboard.storage import (
    load_database,
    save_database,
    save_article,
    article_exists
)


def main():

    config = load_config()

    feeds = load_feeds()

    database = load_database()


    print("Starting Personal Dashboard")

    new_articles = 0


    for feed in feeds:


        print()

        print("Checking:", feed["name"])


        articles = get_articles(feed)


        for article in articles[:10]:


            if article_exists(
                database,
                article["link"]
            ):

                print(
                    "Already saved:",
                    article["title"]
                )

                continue



            downloaded = download_article(
                article["link"]
            )


            if downloaded is None:

                continue



            record = save_article(
                downloaded,
                article["link"]
            )


            record["source"] = feed["name"]

            record["category"] = feed["category"]

            database["articles"].append(
                record
            )


            new_articles += 1


            print(
                "Saved:",
                article["title"]
            )


    save_database(database)


    print()
    print("--------------------")
    print(
        "New articles:",
        new_articles
    )

    print(
        "Total articles:",
        len(database["articles"])
    )


if __name__ == "__main__":

    main()
