from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^new$', views.new_photo, name="newphoto"),
	url(r'^$', views.album_main, name="album"),
)
