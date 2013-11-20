from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'pyta.views.home_view', name='home'),
    url(r'^index$', 'pyta.views.home_view', name='home'),
    url(r'^edit$', 'pyta.views.edit_view', name='edit'),
    url(r'^edit_ajax', 'pyta.views.edit_view_ajax', name='edit_ajax'),
    url(r'^edit_request_priority$',
        'pyta.views.set_request_priority_view_ajax',
        name='edit_request_priority'),
    url(r'^login$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, name='logout',),
    url(r'^requests$', 'pyta.views.requests_view', name='requests'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
