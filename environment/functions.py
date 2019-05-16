import copy
import sys

WIDTH = 7
HEIGHT = 6
EMPTY = ' '
WHITE = 'O'
BLACK = 'X'
INF = 10000000
character = dict()
character[WHITE] = 'O'
character[BLACK] = 'X'
character[EMPTY] = ' '

def printf(format, *args):
    sys.stdout.write(format % args)

def get_initial_state():
    return tuple([() for i in range(7)])

def get_oponent_color(my_color):
    return BLACK if my_color == WHITE else WHITE
    # return my_color*-1

def get_next_state(state, action, color):
    ns = [c for c in state]
    nc = list(ns[action])
    nc.append(color)
    ns[action] = tuple(nc)
    return tuple(ns)

def get_legal_actions(state):
    actions = []
    for i, c in enumerate(state):
        if len(c) < 6:
            actions.append(i)
    return actions

def print_state(state):
    s = [list(c) for c in state]
    for c in s:
        while len(c) < HEIGHT:
            c.append(EMPTY)
    for h in reversed(range(HEIGHT)):
        printf('| ')
        for w in range(WIDTH):
            printf('%s ', character[s[w][h]])
        print('|')
    print('  1 2 3 4 5 6 7')


