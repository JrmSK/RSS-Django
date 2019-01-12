from django.shortcuts import render, HttpResponse
from datetime import datetime
import ssl
from .utils import get_headlines, save_headlines, RSS_FEEDS
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import Headlines


# necessary for mac users
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def index(request):

    # desired_rss_feed = request.GET.get("feed")
    # if desired_rss_feed not in RSS_FEEDS:
    #     desired_rss_feed = "1"
    #
    # headlines = get_headlines(desired_rss_feed)
    #
    # return render(request, 'rss/rss.html', {"headlines": headlines})
    first_visit = "stranger"
    if request.user.is_authenticated():
        first_visit = "back, {}".format(request.user.username)
    response = render(request, 'rss/welcome.html', {'first_visit': first_visit})
    response.set_cookie("visited_at", str(datetime.now()), max_age=3600 * 24)
    return response


@login_required
def feeds(request):
    result = ['{}: {} - {}'.format(feed, RSS_FEEDS[feed]['title'], RSS_FEEDS[feed]['rss_link']) for feed in RSS_FEEDS]
    print(result)
    return render(request, 'rss/chooseFeed.html', {'result': result})


@login_required
def headlines(request):
    desired_rss_feed = request.GET.get("feed")
    if desired_rss_feed not in RSS_FEEDS:
        desired_rss_feed = "1"

    headlines = get_headlines(desired_rss_feed)
    save_headlines(headlines)
    response = render(request, 'rss/headlines.html', {'headlines': headlines})
    response.set_cookie("visited_at", str(datetime.now()), max_age=3600 * 24)

    return response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return index(request)
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def search(request):
    query = request.POST.get('find_headlines').split(' ')
    search_result = Headlines.objects.filter(title__icontains=query[0]).order_by('time_added')
    if len(query) > 1:
        for i in range(1, len(query)):
            search_result = search_result.filter(title__icontains=query[i])
    return render(request, 'rss/search.html', {'context': search_result})
