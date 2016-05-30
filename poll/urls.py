from django.conf.urls import patterns, url
from poll.views import *

urlpatterns = patterns('poll.views',

    url(r'^api/v1/register/$', RegisterView.as_view()),
    url(r'^registration_confirmation/(?P<registration_hash>\w+)', RegisterView.as_view()),
    url(r'^api/v1/login/$', LoginView.as_view()),
    url(r'^api/v1/logout/$', LoginView.as_view()),
    url(r'^$', IndexView.as_view()),
)