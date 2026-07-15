"""
RSS downloader
Downloads article information from RSS feeds.
"""

import feedparser


def get_articles(feed):

    print(f"\nChecking {feed['name']}...")

    rss = feedparser.parse(feed["url"])

    if rss.bozo:
        print("  WARNING: Feed may have errors.")

    articles = []

    for entry in rss.entries:

        article = {
            "source": feed["name"],
            "category": feed["category"],
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        }

        articles.append(article)

    print(f"  Found {len(articles)} articles.")

    return articles
