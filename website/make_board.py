# -*- coding:utf-8 -*-
from django.contrib.auth.models import User

from board.models import Board

## MAKE BOARDS ##
board_list = [
    'HeXA','History','Member','Calender','CTF','Gallery',
    'Notice','Update','FreeBoard','Gallery2',
    'System1','Network1','Web1','Other',
    'System2','Network2','Web2','Coding','Information',
    'Rank','Game'
]

for name in board_list:
    b = Board(name=name, readable=0, writable=0)
    b.save()
