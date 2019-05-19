#!/usr/bin/env python3
from environment import *
from algorithms import *

# state = (('O', 'X', 'O', 'O', 'X', 'O'), ('X', 'X', 'O', 'X', 'X', 'O'), ('O', 'X', 'O', 'X', 'X', 'O'), ('X', 'O', 'X', 'X', 'O', 'X'), ('O', 'O', 'X', 'O', 'O', 'X'), (), ('O', 'X', 'O', 'X'))
#
# print_state(state)
# algo = AlphaBetaAlgorithm(WHITE)
# color = WHITE
# moves = [6, 5, 6, 5]
# for a in moves:
#     state = get_next_state(state, a, color)
#     color = get_oponent_color(color)

start = 1

state = get_initial_state()
state = get_next_state(state, start, WHITE)
state = get_next_state(state, start+1, WHITE)
state = get_next_state(state, start+1, WHITE)
state = get_next_state(state, start+2, WHITE)
state = get_next_state(state, start+2, WHITE)
state = get_next_state(state, start+2, WHITE)
state = get_next_state(state, start+3, BLACK)
state = get_next_state(state, start+3, WHITE)
state = get_next_state(state, start+3, WHITE)
state = get_next_state(state, start+3, WHITE)

print_state(state)
proc = SimpleStateProcessor(state)
proc.process()
print(proc.is_terminal())