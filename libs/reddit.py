import os
import requests
from requests.auth import HTTPBasicAuth
from libs import cache
import html
import math

monitored_subreddits = [
    'programming',
    'startups',
    'technology',
    'cscareerquestions',
    'nba',
    'boxing',
]


def access_token():
    access_token = cache.get('reddit-access-token')

    if not access_token:
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=HTTPBasicAuth(
                os.environ.get('REDDIT_CLIENT_ID'),
                os.environ.get('REDDIT_CLIENT_SECRET'),
            ),
            headers={'user-agent': 'johanli.com'},
            data={'grant_type': 'client_credentials'},
        )

        access_token = response.json()['access_token']
        cache.set('reddit-access-token', access_token, 3000)

    return access_token


def get_subreddits(bust_cache=False):
    if bust_cache:
        subreddits = []
    else:
        subreddits = cache.get('reddit-subreddits') or []

    if not subreddits:
        for subreddit in monitored_subreddits:
            posts = get_posts(subreddit)
            subreddits.append({
                'name': subreddit,
                'posts': posts,
            })

        cache.set('reddit-subreddits', subreddits, 7200)

    return subreddits


def get_posts(subreddit):
    response = requests.get(
        'https://oauth.reddit.com/r/' + subreddit + '/hot/.json',
        headers={
            'user-agent': 'johanli.com',
            'Authorization': 'bearer ' + access_token(),
        },
        params={
            'limit': 10,
        },
    )

    posts = []

    for post in response.json()['data']['children']:
        data = post['data']

        if data['stickied']:
            continue

        posts.append({
            'title': html.unescape(data['title']),
            'score': format_score(data['score']),
            'number_comments': data['num_comments'],
            'created': data['created_utc'],
            'url': data['url'],
            'comments_url': 'https://www.reddit.com' + data['permalink'],
        })

    return posts


def format_score(score):
    k = score / 1000

    if k >= 10:
        k_one_decimal = math.floor(k * 10) / 10
        return str(k_one_decimal) + 'k'

    return score
