from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'api/feeds/$', views.feeds, name='feeds'),
    url(r'api/headlines/$', views.headlines, name='headlines'),
]