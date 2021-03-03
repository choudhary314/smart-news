import pickle
from flask import Flask, render_template


entries = []
app = Flask(__name__, static_folder="C:\\Users\\tarun\\PycharmProjects\\smart_news\\static")


class RSS:
    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def main():
    with open("news.pkl", "rb") as f:
        news = pickle.load(f)
        f.close()
    return news


def crypto():
    with open("news-crypto.pkl", "rb") as f:
        news = pickle.load(f)
        f.close()
    return news


@app.route("/")
def index():
    return render_template("index.html", foobar=main())


@app.route("/cryptocurrency")
def cryptocurrency():
    return render_template("crypto.html", foobar=crypto())


@app.route("/comingsoon")
def comingsoon():
    return render_template("coming.html")


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
