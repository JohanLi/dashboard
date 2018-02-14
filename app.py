from flask import Flask
from flask import render_template
from libs import reddit
from libs import hackernews
from libs.time_ago import time_ago

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        'index.html',
        subreddits=reddit.getSubreddits(),
        topStories=hackernews.getTopStories(),
    )


app.jinja_env.filters['time_ago'] = time_ago
