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

        print(

            feed["name"],

            "-",

            feed["category"]

        )

if __name__ == "__main__":

    main()
