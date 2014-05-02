from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from intro.views import main

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dinger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', main),
    url(r'^intro/', include('intro.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
