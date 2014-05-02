#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.html import escape

from member.forms import RegisterForm

INTRODUCTION = """
2011년에 만들어진 UNIST의 컴퓨터 정보보안 동아리인 HeXA는 Hacker's eXciting Academy의 약자이며, 컴퓨터 보안에 대한 깊은 연구에 관심을 두고 있는 동아리 입니다.<br>
해킹이라는 말을 컴퓨터 자체로써도 받아들여 컴퓨터의 내부구조에 대한 깊은 공부를 하기도 하고 웹 분야에서의 친숙한 웹 해킹 또한 다루고 있습니다.<br>
때로는, 학교내의 보안 취약점들을 찾아 학교에 보고하면서, 학교의 보안을 강화하기 위해 노력하고 있습니다.<br>
게시판은 승인후 이용가능합니다.<br>
가입후 이름과 아이디를 임원에게 알려주시면 승인해드리겠습니다.<br><br>
연락처<br>
문의 사항은 아래의 E-Mail로 보내 주세요. <br>
회장 한명균: hmg0228@unist.ac.kr
"""

def main(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/intro')

	# render hexa hompage main here.
	return render(request, 'index.html')

def intro(request):
	form = RegisterForm()
	print escape(INTRODUCTION)
	return render(request, 'intro.html', {
			'form': form,
	})

