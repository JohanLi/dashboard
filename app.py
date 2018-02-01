from flask import Flask
from flask import render_template
from libs import reddit
from libs.time_ago import time_ago

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template(
        'reddit.html',
        subreddits=reddit.getSubreddits(),
        time_ago=time_ago,
    )
