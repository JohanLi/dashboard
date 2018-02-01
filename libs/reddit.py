import os
import requests
from requests.auth import HTTPBasicAuth
from libs import cache
import html

monitoredSubreddits = [
    'programming',
    'startups',
    'technology',
    'cscareerquestions',
    'nba',
    'boxing',
]


def accessToken():
    accessToken = cache.get('reddit-access-token')

    if not accessToken:
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=HTTPBasicAuth(
                os.environ.get('REDDIT_CLIENT_ID'),
                os.environ.get('REDDIT_CLIENT_SECRET'),
            ),
            headers={'user-agent': 'johanli.com'},
            data={'grant_type': 'client_credentials'},
        )

        accessToken = response.json()['access_token']
        cache.set('reddit-access-token', accessToken, 3000)

    return accessToken


def getSubreddits():
    subreddits = cache.get('reddit-subreddits') or []

    if not subreddits:
        for subreddit in monitoredSubreddits:
            posts = getPosts(subreddit)
            subreddits.append({
                'name': subreddit,
                'posts': posts,
            })

        cache.set('reddit-subreddits', subreddits, 900)

    return subreddits


def getPosts(subreddit):
    response = requests.get(
        'https://oauth.reddit.com/r/' + subreddit + '/hot/.json',
        headers={
            'user-agent': 'johanli.com',
            'Authorization': 'bearer ' + accessToken(),
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
            'score': data['score'],
            'number_comments': data['num_comments'],
            'created': data['created_utc'],
            'url': data['url'],
            'comments_url': 'https://www.reddit.com' + data['permalink'],
        })

    return posts
