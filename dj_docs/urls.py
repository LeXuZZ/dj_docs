from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('poll_auth.urls', namespace='poll_auth')),
    url(r'^', include('poll.urls', namespace='poll')),
]
