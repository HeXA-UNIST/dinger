# -*- coding: utf-8 -*-
import os
import uuid
import mimetypes
import urllib

from django import template
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .forms import ArticleForm
from .forms import CommentForm
from .models import Board
from .models import Article
from .models import Comment
from .models import Attachment

register = template.Library()

# Create your views here.
def get_board_from_name(name):
    try:
        board = Board.objects.get(name=name)
    except Board.DoesNotExist:
        return None
    return board

@login_required
def list_articles(request, board_name):
    
    board = get_object_or_404(Board, name=board_name)
    return render(request, 'list_articles.html', {
            'current_board': board_name,
            'articles': reversed(board.article_set.all()),
    })

@login_required
def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.hit += 1
    article.save()
    
    board = article.board;

    #if article.read > request.user.authorization:
    # Authorization need
    #   pass


    return render(request, 'list_articles.html', {
            'current_board': board.name,
            'articles': reversed(board.article_set.all()),
            'article': article,
            'is_liked': article.is_liked_by(request.user),
            'comments': article.comment_set.all(),
            'form': CommentForm(),
    })

@login_required
def write_article(request, board_name):
    board = get_object_or_404(Board, name=board_name)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            private = form.cleaned_data['private']
            file = request.FILES
    
            article = Article(subject=subject, content=content, private=private, 
                            board=board, author=request.user)
            article.save()
            
            if file:
                filename = str(file['file'])
                attach = Attachment(name=filename, uuid=uuid.uuid1().hex, file=file['file'], article=article)
                attach.save()

            return HttpResponseRedirect(reverse('article', 
                                        args=[str(article.id)]))
    else:
        form = ArticleForm()

    return render(request, 'write_article.html', {
        'current_board': board_name,
        'form': form,
    })

@login_required
@require_POST
def write_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        Comment.objects.create(content=content, article=article, 
                            author=request.user)

        return HttpResponseRedirect(reverse('article', 
                                        args=[str(article.id)]))
    return HttpResponseRedirect('/')

@login_required
def likes(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.liked_by.add(request.user)
    return HttpResponseRedirect(reverse('article', 
                                    args=[str(article.id)]))
@login_required
def dislikes(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.liked_by.remove(request.user)
    return HttpResponseRedirect(reverse('article', 
                                    args=[str(article.id)]))


@login_required
def download(request, key):
    attach = get_object_or_404(Attachment, uuid=key)

    path = attach.file.path
    filename = unicode(attach.name)
    wrapper = FileWrapper(file(path))
    content_type = mimetypes.guess_type(path)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename.encode('utf-8')
    return response
