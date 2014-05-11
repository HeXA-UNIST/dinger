# -*- coding:utf-8 -*-
from django.contrib.auth.models import User

from board.models import Board

## MAKE BOARDS ##
board_list = [
    'hexa','history','member','calender','ctf',
    'notice','update','freeboard','gallery',
    'system','network','web','other',
    'dbsystem','dbnetwork','dbweb','coding','information',
    'rank','game' 
]

for name in board_list:
    b = Board(name=name, readable=0, writable=0)
    b.save()
