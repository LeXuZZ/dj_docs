from django.conf.urls import url
from poll_auth.views import *

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/(?P<registration_hash>\w{50})', RegisterView.as_view(), name='registration_confirmation'),
    url(r'^password_recovery/$', PasswordRecoveryView.as_view(), name='password_recovery'),
    url(r'^password_recovery/(?P<recovery_hash>\w+)$', PasswordRecoveryView.as_view(),name='password_recovery_confirmation'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
