"""
Parses through all the different Rss feeds stored in feeds.csv and looks for articles matching triggers
in triggers.csv for finance news and then triggers-crypto.csv for crypto news articles. Eventually the matches are stores in a pickled file.
This needs to run as a scheduled task on the server to keep the news.pkl and news-crypto.pkl latest.
"""
import feedparser
import csv
import hashlib
import pickle
import os
from logger import setup_custom_logger

entries = []
log = setup_custom_logger(__file__)
script_dir = os.path.dirname(__file__)


class Rss:
    """
    Class to store the attributes of the articles, and then pickle them
    """

    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def trigger_normalizer(file):
    """
    This is used to load all the trigger words from triggers.csv and add to normalized array.
    """
    normalized = []
    try:
        with open(file) as csv_file:
            triggers = csv.reader(csv_file)
            for trigger in triggers:
                trigger = str(trigger[0])
                normalized.append(trigger.lower())
            return normalized
    except Exception as err:
        log.error(f"Failed to process trigger files for conversion: {err}")
        raise


def rss_parser(url):
    """
    Parses through all the rss feed urls stores them in entries as Rss class objects.
    """
    try:
        data = feedparser.parse(url)
        for i in range(len(data.entries)):
            try:
                ent = Rss(data.entries[i].title, data.entries[i].link)
                entries.append(ent)
            except Exception as err:
                log.warning(
                    f"One or more property not found while parsing rss objects, Skipping!: {err}"
                )
    except Exception as err:
        log.error(f"{url} : rss feed couldn't be parsed: {err}")
        raise


def store_finance():
    """
    Creates the pickle file of the finance articles after finding the match
    Note: The absolute paths need to be converted to relative paths using flask environment variables
    """
    dup_cache = []
    fil_coll = []
    log.info("Finance triggers sync started")
    triggers_path = os.path.join(script_dir, "triggers.csv")
    feeds_path = os.path.join(script_dir, "feeds.csv")
    pkl_path = os.path.join(script_dir, "news.pkl")
    try:
        with open(feeds_path) as csv_file:
            feeds = csv.reader(csv_file)
            for feed in feeds:
                rss_parser(feed[0])
            for entry in entries:
                """This is a brute force way, this can be optimized further by not looping through twice. Work in progress"""
                for i in trigger_normalizer(triggers_path):
                    if i in ((entry.title).lower()).split():
                        if (
                            str((hashlib.md5(entry.title.encode())).hexdigest())
                            not in dup_cache
                        ):
                            dup_cache.append(
                                (hashlib.md5(entry.title.encode())).hexdigest()
                            )
                            entry.trigger = (str(i)).title()
                            filtered = Rss(entry.title, entry.link, entry.trigger)
                            fil_coll.append(filtered)
    except Exception as err:
        log.error(f"feeds file not found for store_finance: {err}")
        raise
    try:
        with open(pkl_path, "wb") as d:
            pickle.dump(fil_coll, open(pkl_path, "wb"))
            log.info("Data dumped in news.pkl, finance triggers synced")
    except Exception as err:
        log.error(f"Pickle file dump for finance errored out: {err}")
        raise


def store_crypto():
    """
    Creates the crypto news related pickle file after finding the match
    Note: The absolute paths need to be converted to relative paths using flask environment variables
    """
    dup_cache = []
    fil_coll = []
    log.info("Crypto triggers sync started")
    crypto_triggers_path = os.path.join(script_dir, "triggers-crypto.csv")
    feeds_path = os.path.join(script_dir, "feeds.csv")
    crypto_pkl_path = os.path.join(script_dir, "news-crypto.pkl")
    try:
        with open(feeds_path) as csv_file:
            feeds = csv.reader(csv_file)
            for feed in feeds:
                rss_parser(feed[0])
            for entry in entries:
                for i in trigger_normalizer(crypto_triggers_path):
                    if i in ((entry.title).lower()).split():
                        if (
                            str((hashlib.md5(entry.title.encode())).hexdigest())
                            not in dup_cache
                        ):
                            dup_cache.append(
                                (hashlib.md5(entry.title.encode())).hexdigest()
                            )
                            entry.trigger = (str(i)).title()
                            filtered = Rss(entry.title, entry.link, entry.trigger)
                            fil_coll.append(filtered)
    except Exception as err:
        log.error(f"feeds file not found for store_finance: {err}")
        raise
    try:
        with open(crypto_pkl_path, "wb") as d:
            pickle.dump(fil_coll, open(crypto_pkl_path, "wb"))
            log.info("Data dumped in news-crypto.pkl, crypto triggers synced")
    except Exception as err:
        log.error(f"Pickle file dump for crypto errored out: {err}")
        raise


if __name__ == "__main__":
    store_finance()
    store_crypto()