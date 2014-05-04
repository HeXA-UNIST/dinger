#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.html import escape

from member.forms import RegisterForm

from board.models import Board

def main(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/intro')

	# render hexa hompage main here.

	return render(request, 'index.html', {
			'boards': Board.objects.all(),
	})

def intro(request):
	form = RegisterForm()
	return render(request, 'intro.html', {
			'form': form,
	})

