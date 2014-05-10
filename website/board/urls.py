from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'^list/(?P<board_name>\w+)$', r, name="list_articles"),
	url(r'^write/(?P<board_name>\w+)$', r, name="write_article"),
	url(r'^article/(?P<article_id>[0-9]+?)$', r, name="view_article"),

    url(r'^([\w]+)/', views.show_board),
)
