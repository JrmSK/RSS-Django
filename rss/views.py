from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import ssl
from .utils import get_headlines, headlines_formater, save_headlines, RSS_FEEDS

# necessary for mac users
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


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

    visited_at = request.COOKIES.get('visited_at')


    headlines = get_headlines(desired_rss_feed)
    formated_headlines = headlines_formater(headlines, visited_at)
    save_headlines(headlines)

    response = HttpResponse(formated_headlines)
    response.set_cookie("visited_at", str(datetime.now()), max_age=3600 * 24)

    return response
