import requests
import html
from libs import cache


def getTopStories():
    topStories = cache.get('hackernews-topstories') or []

    if not topStories:
        for topStoryId in getTopStoryIds()[:20]:
            response = requests.get(
                'https://hacker-news.firebaseio.com/v0/item/' + str(topStoryId) + '.json',
                headers={
                    'user-agent': 'johanli.com',
                },
            )

            topStory = response.json()

            topStories.append({
                'title': html.unescape(topStory['title']),
                'score': topStory['score'],
                'number_comments': topStory.get('descendants'),
                'created': topStory['time'],
                'url': topStory.get('url'),
                'comments_url': 'https://news.ycombinator.com/item?id=' + str(topStory['id']),
            })

        cache.set('hackernews-topstories', topStories, 7200)

    return topStories


def getTopStoryIds():
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json',
        headers={
            'user-agent': 'johanli.com',
        },
    )

    return response.json()
