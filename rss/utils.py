import feedparser
from .models import Headlines
from datetime import datetime

RSS_FEEDS = {
    "1": {
        "title": "The Jerusalem Post",
        "rss_link": "https://www.jpost.com/Rss/RssFeedsHeadlines.aspx"
    },
    "2": {
        "title": "Daily Mail",
        "rss_link": "http://www.dailymail.co.uk/articles.rss"
    },
    "3": {
        "title": "Wired Magazine",
        "rss_link": "http://feeds.wired.com/wired/index"
    },
}

def get_headlines(desired_rss_feed):

    # Fetch the feed
    feed = feedparser.parse(RSS_FEEDS[desired_rss_feed]["rss_link"])

    headlines = [
        {"title": entry["title"], "link": entry["link"]}
        for entry in feed["entries"]
    ]
    return headlines


def headlines_formater(headlines):
    result = ' '.join([
        '<li>{} - <a href={}>link</a></li>'.format(obj['title'], obj['link'])
        for obj in headlines
    ])
    return result


def save_headlines(headlines):
    count = 0
    for obj in headlines:
        if not Headlines.objects.filter(title=obj['title']).exists():
            headline = Headlines(title=obj['title'], link=obj['link'], time_added=datetime.now())
            headline.save()
    return '{} headlines saved to DB'.format(count)
