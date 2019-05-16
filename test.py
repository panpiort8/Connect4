#!/usr/bin/env python3
from environment import *
from algorithms import *

state = (('O', 'X', 'O', 'O', 'X', 'O'), ('X', 'X', 'O', 'X', 'X', 'O'), ('O', 'X', 'O', 'X', 'X', 'O'), ('X', 'O', 'X', 'X', 'O', 'X'), ('O', 'O', 'X', 'O', 'O', 'X'), (), ('O', 'X', 'O', 'X'))

print_state(state)
algo = AlphaBetaAlgorithm(WHITE)
color = WHITE
moves = [6, 5, 6, 5]
for a in moves:
    state = get_next_state(state, a, color)
    color = get_oponent_color(color)

print()
print_state(state)
print(moves)
proc = AlphaStateProcessor()
proc.process(state)
print(proc.isTerminal())
print(algo.utility(proc))