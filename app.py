import settings
from flask import Flask
from flask import render_template
from libs.reddit import get_subreddits
from libs.hackernews import get_top_stories
from libs.weather import forecast
from libs.filters.time_ago import time_ago

app = Flask(__name__)


@app.route("/")
def reddit():
    return render_template(
        'reddit.html',
        subreddits=get_subreddits(),
        section='reddit',
    )


@app.route("/hackernews")
def hackernews():
    return render_template(
        'hackernews.html',
        top_stories=get_top_stories(),
        section='hackernews',
    )


@app.route("/misc")
def misc():
    return render_template(
        'misc.html',
        forecast=forecast(),
        section='misc',
    )


app.jinja_env.filters['time_ago'] = time_ago
