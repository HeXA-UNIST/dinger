from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^new$', views.new_photo, name="newphoto"),
    
     # ajax interface
    url(r'^list$', views.ajax_request_albums),
    url(r'^photos$', views.ajax_request_photos),
    
    
    
    url(r'^(?P<photo_id>[0-9]+?)$', views.photo, name="photo"),
    url(r'^t/(?P<photo_id>[0-9]+?)$', views.thumbnail, name="thumbnail"),
    url(r'^$', views.album_main, name="album"),

)
