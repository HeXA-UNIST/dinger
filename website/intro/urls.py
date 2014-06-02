from django.conf.urls import patterns, include, url

from intro import views

urlpatterns = patterns('',
	url(r'^$', views.intro, name="intro"),
	url(r'^login', views.login, name="login"),
)
