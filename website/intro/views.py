#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.html import escape

from member.forms import RegisterForm

from board.models import Board

@login_required
def main(request):
	# render hexa hompage main here.

	return render(request, 'index.html', {
			'boards': Board.objects.all(),
	})

def intro(request):
	form = RegisterForm()
	return render(request, 'intro.html', {
			'form': form,
	})

def login(request):
	form = RegisterForm()
	return render(request, 'login.html', {
			'form': form,
	})
