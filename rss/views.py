from django.http import HttpResponse
from django.shortcuts import render
import json
import feedparser


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
    desired_rss_feed = request.query.get("feed", "1")
    if desired_rss_feed not in RSS_FEEDS:
        desired_rss_feed = '1'
    return HttpResponse(response)
