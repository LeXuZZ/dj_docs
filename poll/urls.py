from django.conf.urls import patterns, url
from poll.views import *

urlpatterns = [
    url(r'^api/v1/poll/$', PollView.as_view()),
    url(r'^api/v1/poll/(?P<id>\d+)/$', PollView.as_view()),
    url(r'^api/v1/get_csrf_token/$', get_csrf),
    url(r'^api/v1/register/$', RegisterView.as_view()),
    url(r'^api/v1/registration_confirmation/(?P<registration_hash>\w+)', RegisterView.as_view()),
    url(r'^api/v1/login/$', LoginView.as_view()),
    url(r'^api/v1/logout/$', LoginView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^register/(?P<registration_hash>.*)$', RegisterView.as_view()),
    url(r'^$', login_required(IndexView.as_view(), login_url='/login/')),
]