"""
This is the entry point into the app, serves the webpage instance by unpickling the article collections
"""
import pickle
import os
from flask import Flask, render_template
from logger import setup_custom_logger

log = setup_custom_logger(__file__)
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))


class Rss:
    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def main():
    """
    Unpickles the finance-news Rss objects
    """
    try:
        with open("news.pkl", "rb") as f:
            news = pickle.load(f)
            f.close()
    except Exception as err:
        log.error(f"news.pkl could't be unpicked: {err}")
    return news


def crypto():
    """
    Unpickles the cryptocurrency-news Rss objects
    """
    try:
        with open("news-crypto.pkl", "rb") as f:
            crypto_news = pickle.load(f)
            f.close()

    except Exception as err:
        log.error(f"news-crypto.pkl unpickling error'd out: {err}")
    return crypto_news


@app.route("/")
def index():
    """
    Serves the finance/landing page
    """
    try:
        return render_template("index.html", foobar=main())
    except Exception as err:
        log.error(f"couldn't render the finance/landing page: {err}")


@app.route("/cryptocurrency")
def cryptocurrency():
    """
    Serves the crptocurrency page
    """
    try:
        return render_template("crypto.html", foobar=crypto())
    except Exception as err:
        log.error(f"couldn't render the crypto page: {err}")


@app.route("/comingsoon")
def comingsoon():
    """
    Serves the commingsoon page
    """
    try:
        return render_template("coming.html")
    except Exception as err:
        log.error(f"couldn't render the coming soon page: {err}")


@app.route("/login")
def login():
    """
    Serves the login page
    """
    try:
        return render_template("loginview.html")
    except Exception as err:
        log.error(f"couldn't render the login page: {err}")


if __name__ == "__main__":
    try:
        app.jinja_env.cache = {}
        app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
    except Exception as err:
        log.error(f"flask app errored out with: {err}")