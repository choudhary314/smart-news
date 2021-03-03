import pickle
from flask import Flask, render_template


entries = []
app = Flask(__name__, static_folder="/var/www/html/static")


class RSS:
    def __init__(self, title, link, trigger="none"):
        self.title = title
        self.link = link
        self.trigger = trigger


def main():
    with open("/var/www/html/news.pkl", "rb") as f:
        news = pickle.load(f)
        f.close()
    return news


@app.route("/")
def index():
    return render_template("index.html", foobar=main())


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
