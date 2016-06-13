from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from poll.views import *

urlpatterns = [
    url(r'^api/v1/poll/$', PollView.as_view()),
    url(r'^api/v1/poll/(?P<id>\d+)/$', PollView.as_view()),
    url(r'^api/v1/get_csrf_token/$', get_csrf),
    url(r'^$', login_required(IndexView.as_view(), login_url='/auth/login/')),
]
