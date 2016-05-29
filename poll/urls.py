from django.conf.urls import patterns, url
from poll.views import *

urlpatterns = patterns('poll.views',

    url(r'^$', IndexView.as_view()),
)