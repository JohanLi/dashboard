from flask import Flask
from flask import render_template
from libs.reddit import getSubreddits
from libs.hackernews import getTopStories
from libs.filters.time_ago import time_ago

app = Flask(__name__)


@app.route("/")
def reddit():
    return render_template(
        'reddit.html',
        subreddits=getSubreddits(),
        section='reddit',
    )


@app.route("/hackernews")
def hackernews():
    return render_template(
        'hackernews.html',
        topStories=getTopStories(),
        section='hackernews',
    )


app.jinja_env.filters['time_ago'] = time_ago
