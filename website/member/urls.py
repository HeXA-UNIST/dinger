from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^signin$', views.sign_in, name="signin"),
	url(r'^signup$', views.sign_up, name="signup"),
	url(r'^signout$', views.sign_out, name="signout"),
)
