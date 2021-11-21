import feedparser
import csv
import hashlib
import pickle

entries = []


class RSS:
    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def feed_urls(file):
    with open(file) as csv_file:
        collection = csv.reader(csv_file)
        return collection


def trigger_normalizer(file):
    normalized = []
    with open(file) as csv_file:
        triggers = csv.reader(csv_file)
        for trigger in triggers:
            trigger = str(trigger[0])
            normalized.append(trigger)
            normalized.append(trigger.capitalize())
            normalized.append(trigger.lower())
            normalized.append(trigger.upper())
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
    dup_cache = []
    fil_coll = []
    with open("feeds.csv") as csv_file:
        feeds = csv.reader(csv_file)
        for feed in feeds:
            rss_parser(feed[0])
    for entry in entries:
        for i in trigger_normalizer("triggers.csv"):
            if i in entry.title:
                if (
                    str((hashlib.md5(entry.title.encode())).hexdigest())
                    not in dup_cache
                ):
                    dup_cache.append(
                        (hashlib.md5(entry.title.encode())).hexdigest())
                    entry.trigger = (str(i)).title()
                    filtered = RSS(entry.title, entry.link, entry.trigger)
                    fil_coll.append(filtered)
    with open("news.pkl", "wb") as d:
        pickle.dump(fil_coll, open("news.pkl", "wb"))
        print("data dumped, finance triggers synced")
        d.close()


def store_crypto():
    dup_cache = []
    fil_coll = []
    with open("feeds.csv") as csv_file:
        feeds = csv.reader(csv_file)
        for feed in feeds:
            rss_parser(feed[0])
    for entry in entries:
        for i in trigger_normalizer("triggers-crypto.csv"):
            if i in (entry.title).split(' '):
                if (
                    str((hashlib.md5(entry.title.encode())).hexdigest())
                    not in dup_cache
                ):
                    dup_cache.append(
                        (hashlib.md5(entry.title.encode())).hexdigest())
                    entry.trigger = (str(i)).title()
                    filtered = RSS(entry.title, entry.link, entry.trigger)
                    fil_coll.append(filtered)
    with open("news-crypto.pkl", "wb") as d:
        pickle.dump(fil_coll, open("news-crypto.pkl", "wb"))
        print("data dumped, crypto triggers synced")
        d.close()


if __name__ == "__main__":
    store_finance()
    store_crypto()
