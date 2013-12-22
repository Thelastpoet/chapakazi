from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^chapakazi/', include('chapa.urls', namespace='chapakazi')),
    url(r'^admin/', include(admin.site.urls)),
    # The views below are for the django registration
    # url(r'^accounts/', include('registration.backends.default.urls', namespace='accounts')),
    url(r'^accounts/', include('profiles.urls', namespace='accounts')),
    
)

