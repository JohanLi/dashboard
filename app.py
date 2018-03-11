import settings
from flask import Flask, render_template, jsonify, request
from libs.reddit import get_subreddits
from libs.hackernews import get_top_stories
from libs.weather import forecast
from libs.plants import get_plants, water
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
        plants=get_plants(),
        section='misc',
    )


@app.route("/plants/water", methods=['PUT'])
def plants_water():
    plant_id = int(request.get_json()['id'])
    water(plant_id)

    return jsonify({
        'success': True,
    })


app.jinja_env.filters['time_ago'] = time_ago