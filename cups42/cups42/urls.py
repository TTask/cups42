from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pyta.views.home_view', name='home'),
    url(r'^index$', 'pyta.views.home_view', name='home'),
    url(r'^edit$', 'pyta.views.edit_view', name='edit'),
    url(r'^login$', 'pyta.views.login_view', name='login'),
    url(r'^logout$', 'pyta.views.logout_view', name='logout'),
    url(r'^requests$', 'pyta.views.requests_view', name='requests'),
    url(r'^admin/', include(admin.site.urls)),
)
