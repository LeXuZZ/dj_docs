from django.conf.urls import url
from poll_auth.views import *


urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^registration_confirmation/(?P<registration_hash>\w+)', RegisterView.as_view(),
        name='registration_confirmation'),
    url(r'^password_recovery/$', PasswordRecoveryView.as_view(), name='password_recovery'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
