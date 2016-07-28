from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from poll.views import *

urlpatterns = [
    url(r'^api/v1/poll/$', login_required(PollView.as_view())),
    url(r'^api/v1/poll/(?P<pk>\d+)/$', login_required(PollView.as_view())),
    url(r'^api/v1/get_csrf_token/$', get_csrf),
    url(r'^$', login_required(IndexView.as_view())),
]
