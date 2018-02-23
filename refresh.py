import settings
from libs.reddit import get_subreddits
from libs.hackernews import get_top_stories
from libs.weather import get_weather

get_subreddits(True)
get_top_stories(True)
get_weather(True)
