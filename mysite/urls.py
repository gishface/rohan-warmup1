from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
	(r'^login2/$', 'auth.views.login_user'),
    (r'^', 'lauth.views.login_user'),
    url(r'^admin/', include(admin.site.urls)),
)