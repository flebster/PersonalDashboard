from dashboard.webbuilder import build_web_dashboard
from dashboard.config import load_config
from dashboard.feeds import load_feeds
from dashboard.downloader import get_articles
from dashboard.article import download_article
from dashboard.storage import (
    load_database,
    save_database,
    article_exists
)


def main():

    config = load_config()

    feeds = load_feeds()

    database = load_database()


    print("Starting Personal Dashboard")

    new_articles = 0
    blocked_articles = 0
    failed_articles = 0


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

            print(article)
            result = download_article(article)


            if result["status"] == "blocked":

                print(
                    "Blocked (403):",
                    article["title"]
                )

                blocked_articles += 1

                continue


            if result["status"] != "saved":

                print(
                    "Failed:",
                    article["title"]
                )

                failed_articles += 1

                continue


            record = {

                "id": article.get("id"),

                "title": article["title"],

                "url": article["link"],

                "file": result["file"],

                "downloaded": result.get(
                    "downloaded"
                ),

                "read": False,

                "saved": False,

                "source": feed["name"],

                "category": feed["category"]

            }


            database["articles"].append(
                record
            )


            new_articles += 1


            print(
                "Saved:",
                article["title"]
            )


    save_database(database)

    build_web_dashboard()


    print()
    print("--------------------")
    print(
        "New articles:",
        new_articles
    )

    print(
        "Blocked:",
        blocked_articles
    )

    print(
        "Failed:",
        failed_articles
    )

    print(
        "Total articles:",
        len(database["articles"])
    )


if __name__ == "__main__":

    main()
