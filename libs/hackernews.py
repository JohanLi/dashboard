import requests
import html
from libs import cache


def get_top_stories(bust_cache=False):
    if bust_cache:
        top_stories = []
    else:
        top_stories = cache.get('hackernews-topstories') or []

    if not top_stories:
        for top_story_id in get_top_story_ids()[:20]:
            response = requests.get(
                'https://hacker-news.firebaseio.com/v0/item/' + str(top_story_id) + '.json',
                headers={
                    'user-agent': 'johanli.com',
                },
            )

            top_story = response.json()

            top_stories.append({
                'title': html.unescape(top_story['title']),
                'score': top_story['score'],
                'number_comments': top_story.get('descendants'),
                'created': top_story['time'],
                'url': top_story.get('url'),
                'comments_url': 'https://news.ycombinator.com/item?id=' + str(top_story['id']),
            })

        cache.set('hackernews-topstories', top_stories, 7200)

    return top_stories


def get_top_story_ids():
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json',
        headers={
            'user-agent': 'johanli.com',
        },
    )

    return response.json()
