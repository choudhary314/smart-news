"""
Parses through all the different RSS feeds stored in feeds.csv and looks for articles matching triggers
in triggers.csv for finance news and then triggers-crypto.csv for crypto news articles. Eventually the matches are stores in a pickled file.
This needs to run as a scheduled task on the server to keep the news.pkl and news-crypto.pkl latest.
"""
import feedparser
import csv
import hashlib
import pickle

entries = []


class RSS:
    """Class to store the attributes of the articles, and then pickle them"""

    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def feed_urls(file):
    with open(file) as csv_file:
        collection = csv.reader(csv_file)
        return collection


def trigger_normalizer(file):
    """
    This is used to load all the trigger words from triggers.csv and add to normalized array.
    """
    normalized = []
    with open(file) as csv_file:
        triggers = csv.reader(csv_file)
        for trigger in triggers:
            trigger = str(trigger[0])
            normalized.append(trigger.lower())
        return normalized


def rss_parser(url):
    data = feedparser.parse(url)
    for i in range(len(data.entries)):
        try:
            ent = RSS(data.entries[i].title, data.entries[i].link)
        except:
            print("One or more property not found, Skipping!")
        entries.append(ent)


def store_finance():
    """
    Creates the pickle file of the finance articles after finding the match
    Note: The absolute paths need to be converted to relative paths using flask environment variables
    """
    dup_cache = []
    fil_coll = []
    with open("/var/www/html/feeds.csv") as csv_file:
        feeds = csv.reader(csv_file)
        for feed in feeds:
            rss_parser(feed[0])
    for entry in entries:
        """This is a brute force way, this can be optimized further by not looping through twice. Work in progress"""
        for i in trigger_normalizer("/var/www/html/triggers.csv"):
            if i in ((entry.title).lower()).split():
                if (
                    str((hashlib.md5(entry.title.encode())).hexdigest())
                    not in dup_cache
                ):
                    dup_cache.append((hashlib.md5(entry.title.encode())).hexdigest())
                    entry.trigger = (str(i)).title()
                    filtered = RSS(entry.title, entry.link, entry.trigger)
                    fil_coll.append(filtered)
    with open("/var/www/html/news.pkl", "wb") as d:
        pickle.dump(fil_coll, open("/var/www/html/news.pkl", "wb"))
        print("data dumped, finance triggers synced")
        d.close()


def store_crypto():
    """
    Creates the crypto news related pickle file after finding the match
    Note: The absolute paths need to be converted to relative paths using flask environment variables
    """
    dup_cache = []
    fil_coll = []
    with open("/var/www/html/feeds.csv") as csv_file:
        feeds = csv.reader(csv_file)
        for feed in feeds:
            rss_parser(feed[0])
    for entry in entries:
        for i in trigger_normalizer("/var/www/html/triggers-crypto.csv"):
            if i in ((entry.title).lower()).split():
                if (
                    str((hashlib.md5(entry.title.encode())).hexdigest())
                    not in dup_cache
                ):
                    dup_cache.append((hashlib.md5(entry.title.encode())).hexdigest())
                    entry.trigger = (str(i)).title()
                    filtered = RSS(entry.title, entry.link, entry.trigger)
                    fil_coll.append(filtered)
    with open("/var/www/html/news-crypto.pkl", "wb") as d:
        pickle.dump(fil_coll, open("/var/www/html/news-crypto.pkl", "wb"))
        print("data dumped, crypto triggers synced")
        d.close()


if __name__ == "__main__":
    store_finance()
