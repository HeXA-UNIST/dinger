from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from intro.views import main
from board import views as board_views

urlpatterns = patterns('',
    url(r'^$', main, name="index"),
    url(r'^intro/', include('intro.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^album/', include('album.urls')),
   	url(r'^admin/', include(admin.site.urls)),

    url(r'^board/$', board_views.list_all_articles, name="listall"),
	url(r'^board/(?P<board_name>\w+)$', board_views.list_board_articles, name="board"),
	
	url(r'^write/(?P<board_name>\w+)$', board_views.write_article, name="write_article"),
	url(r'^comment/(?P<article_id>[0-9]+?)$', board_views.write_comment, name="comment"),

	url(r'^likes/(?P<article_id>[0-9]+?)$', board_views.likes, name="likes"),
	url(r'^dislikes/(?P<article_id>[0-9]+?)$', board_views.dislikes, name="dislikes"),

	url(r'^download/(?P<key>\w+)$', board_views.download, name="download"),
)
