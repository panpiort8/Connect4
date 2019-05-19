#!/usr/bin/env python3
import algorithms.api as api
import algorithms
import argparse
import sys
import os
import environment as env

algo_base = api.Algorithm
all_algos = [ (name, cls) for name, cls in algorithms.__dict__.items() if
        isinstance(cls, type) and
        issubclass(cls, algo_base) and
        cls != algo_base
    ]

parser = argparse.ArgumentParser(description='Simulate Game')
parser.add_argument('-w', '--white_algorithm', type=str, help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
parser.add_argument('-b', '--black_algorithm', type=str, help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
parser.add_argument('-t', '--time', type=float, default=1.0, help='time of move planning')
parser.add_argument('-p', '--print_moves', action='store_false', default=True, help='print all moves')
args = vars(parser.parse_args())

algos = dict()
algos[env.WHITE] = None
algos[env.BLACK] = None
for name, cls in all_algos:
    if name.lower().startswith(args['white_algorithm'].lower()):
        algos[env.WHITE] = cls
    if name.lower().startswith(args['black_algorithm'].lower()):
        algos[env.BLACK] = cls
if algos[env.WHITE] is None or algos[env.BLACK] is None:
    parser.print_help()
    sys.exit(1)

player = dict()
player[env.WHITE] = algos[env.WHITE](env.WHITE)
player[env.BLACK] = algos[env.BLACK](env.BLACK)

state = env.get_initial_state()
proc = env.SimpleStateProcessor(state)
proc.process()
color = env.WHITE
while not proc.is_terminal():
    if args['print_moves']:
        os.system('clear')
        print('\n\n\n')
    env.print_state(state)
    print("\n{} ({}) IS MOVING...".format('WHITE' if color == env.WHITE else 'BLACK', algos[color].__name__))
    a = player[color].get_action(state, timer=api.Timer(args['time']))
    player[env.WHITE].update_move(a)
    player[env.BLACK].update_move(a)
    state = env.get_next_state(state, a, color)
    proc = env.SimpleStateProcessor(state)
    proc.process()
    color = env.get_oponent_color(color)

if args['print_moves']:
    os.system('clear')
    print('\n\n\n')
env.print_state(state)
if proc.get_winner() == env.WHITE:
    print("WHITE ({}) WON".format(algos[env.WHITE].__name__))
elif proc.get_winner() == env.BLACK:
    print("BLACK ({}) WON".format(algos[env.BLACK].__name__))
else:
    print("DRAW")