from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import json
import feedparser
import ssl
from .models import Headlines

# necessary for mac users
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


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


def index(request):
    return render(request, 'rss/index.html')


def feeds(request):
    result = ['{}: {} - {}'.format(feed, RSS_FEEDS[feed]['title'], RSS_FEEDS[feed]['rss_link']) for feed in RSS_FEEDS]
    print(result)
    return render(request, 'rss/chooseFeed.html', {'result': result})


def headlines(request):
    desired_rss_feed = request.GET.get("feed")
    if desired_rss_feed not in RSS_FEEDS:
        desired_rss_feed = "1"

    # Fetch the feed
    feed = feedparser.parse(RSS_FEEDS[desired_rss_feed]["rss_link"])

    visited_at = request.COOKIES.get('visited_at')

    headlines = [
                    {"title": entry["title"], "link": entry["link"]}
                    for entry in feed["entries"]
                ]

    result = ' '.join([
                        '<li>{} - <a href={}>link</a></li>'.format(obj['title'], obj['link'])
                        for obj in headlines
                    ]) + '<br /> <p>Visited at: {}</p>'.format(visited_at[:-7])

    for obj in headlines:
        if not Headlines.objects.filter(title=obj['title']).exists():
            headline = Headlines(title=obj['title'], link=obj['link'], time_added=datetime.now())
            headline.save()


    response = HttpResponse(result)
    response.set_cookie("visited_at", str(datetime.now()), max_age=3600 * 24)

    return response
