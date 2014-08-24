# -*- coding: utf-8 -*-
import os
import uuid
import mimetypes
import urllib

from django import template
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404 
from django.views.decorators.http import require_POST
from django.utils import html
from django.utils.safestring import mark_safe

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


def esc(art):
    art.content_lines = art.content.split('\n')
    return art
    art.content = ''.join(map(lambda p: p.join(['<p>']*2), art.content.split('\n')))
    # print art.content
    art.content = mark_safe(art.content)
    
    return art

def render_board(request, board, articles):
    pager = Paginator(list(reversed(articles)), 15)
    page = request.GET.get('page')
    try:
        articles = pager.page(page)
    except PageNotAnInteger:
        articles = pager.page(1)
    except EmptyPage:
        articles = pager.page(pager.num_pages)

    article_id = request.GET.get('article', 0)
    try:
        article_id = int(article_id)
    except ValueError:
        article_id = 0
        
    vars = {}
    if board:
        vars.update({'current_board': board.name})
    vars.update({
            'articles': articles,
    })
    if article_id > 0:
        article = get_object_or_404(Article, pk=article_id)
        if board and board != article.board:
            raise Http404("Article Not Found")
            
        vars.update({
            'article': esc(article),
            'is_liked': article.is_liked_by(request.user),
            'comments': article.comment_set.all(),
            'form': CommentForm(),
        })
        
    return render(request, 'list_articles.html', vars)
    
@login_required
def list_all_articles(request):
    return render_board(request, None, Article.objects.all())
    
@login_required
def list_board_articles(request, board_name):    
    board = get_object_or_404(Board, name=board_name)
    return render_board(request, board, board.article_set.all())

    
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
            
            redirect_url = reverse('board', args=[str(article.board.name)])    
            qs = urllib.urlencode({'article': article.id})
            return HttpResponseRedirect('{}?{}'.format(redirect_url, qs))
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
    board_name = request.POST.get('board', None)
    if board_name:
        board = get_object_or_404(Board, name=board_name)
        if board != article.board:
            raise Http404("Article Not Found")
            
    page = request.POST.get('page')
        
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        Comment.objects.create(content=content, article=article, 
                            author=request.user)

    if board:
        redirect_url = reverse('board', args=[str(board_name)])
    else:
        redirect_url = reverse('listall')
    
    qs = urllib.urlencode({'article': article_id, 'page': page})
    return HttpResponseRedirect('{}?{}'.format(redirect_url, qs))
    

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

def download(request, key):
    if request.user.is_anonymous():
        raise Http404
    attach = get_object_or_404(Attachment, uuid=key)
    path = attach.file.path
    filename = unicode(attach.name)
    wrapper = FileWrapper(file(path))
    content_type = mimetypes.guess_type(path)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename.encode('utf-8')
    return response
