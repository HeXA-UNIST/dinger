# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .forms import ArticleForm
from .forms import CommentForm
from .models import Board
from .models import Article
from .models import Comment
from .models import Likes

# Create your views here.

def get_board_from_name(name):
	try:
		board = Board.objects.get(name=name)
	except Board.DoesNotExist:
		return None
	return board

def list_articles(request, board_name):
	
	board = get_object_or_404(Board, name=board_name)
	return render(request, 'list_articles.html', {
			'current_board': board_name,
			'articles': reversed(board.article_set.all()),
	})
	
def view_article(request, article_id):
	article = get_object_or_404(Article, pk=article_id)

	#if article.read > request.user.authorization:
	# Authorization need
	#	pass

	return render(request, 'view_article.html', {
			'article': article,
			'comments': article.comment_set.all(),
			'form': CommentForm(),
	})


def write_article(request, board_name):
	board = get_object_or_404(Board, name=board_name)
	if request.method == "GET":
		form = ArticleForm()
		return render(request, 'write_article.html', {
			'current_board': board_name,
            'form': form,
    	})

	elif request.method == "POST":
		form = ArticleForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			content = form.cleaned_data['content']
			private = form.cleaned_data['private']

			article = Article(subject=subject, content=content, private=private, 
							board=board, author=request.user)
			article.save()
			return HttpResponseRedirect(reverse('view_article', 
										args=[str(article.id)]))
	return HttpResponseRedirect('/')

@require_POST
def write_comment(request, article_id):
	article = get_object_or_404(Article, pk=article_id)
	form = CommentForm(request.POST)
	if form.is_valid():
		content = form.cleaned_data['content']
		Comment.objects.create(content=content, article=article, 
							author=request.user)

		return HttpResponseRedirect(reverse('view_article', 
										args=[str(article.id)]))
	return HttpResponseRedirect('/')



