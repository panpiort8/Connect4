#!/usr/bin/python3
import algorithms.api as api
import algorithms
import argparse
import sys
from environment import *
import progressbar

algo_base = api.Algorithm
all_algos = [ (name, cls) for name, cls in algorithms.__dict__.items() if
        isinstance(cls, type) and
        issubclass(cls, algo_base) and
        cls != algo_base
    ]

parser = argparse.ArgumentParser(description='Simulate Game')
parser.add_argument('-g', '--games', type=int, default=10, help='games to play')
parser.add_argument('-t', '--time', type=float, default=1.0, help='step time in seconds')
parser.add_argument('-y', '--gamma_white', type=float, default=1.0, help='gamma used in MCTree algorithm (for white player)')
parser.add_argument('-z', '--gamma_black', type=float, default=1.0, help='gamma used in MCTree algorithm (for black player)')
parser.add_argument('-r', '--rollouts_white', type=int, default=1, help='rollouts averaged in MCTree algorithm (for white player)')
parser.add_argument('-p', '--rollouts_black', type=int, default=1, help='rollouts averaged in MCTree algorithm (for black player)')
parser.add_argument('-w', '--white_algorithm', type=str,
                    help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
parser.add_argument('-b', '--black_algorithm', type=str,
                    help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
args = vars(parser.parse_args())

algos = dict()
algos[WHITE] = None
algos[BLACK] = None
for name, cls in all_algos:
    if name.lower().startswith(args['white_algorithm'].lower()):
        algos[WHITE] = cls
    if name.lower().startswith(args['black_algorithm'].lower()):
        algos[BLACK] = cls
if algos[WHITE] is None or algos[BLACK] is None:
    parser.print_help()
    sys.exit(1)

player = dict()
player[WHITE] = algos[WHITE](WHITE, gamma=args['gamma_white'], rollouts=args['rollouts_white'])
player[BLACK] = algos[BLACK](BLACK, gamma=args['gamma_black'], rollouts=args['rollouts_black'])

points = dict()
points[WHITE] = 0
points[BLACK] = 0
points[EMPTY] = 0

print("Comparing {} as WHITE and {} as BLACK".format(algos[WHITE].__name__, algos[BLACK].__name__))
widgets = ["Games: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=args['games'], widgets=widgets).start()
for i in range(args['games']):
    state = get_initial_state()
    proc = SimpleStateProcessor(state)
    proc.process()
    color = WHITE
    while not proc.is_terminal():
        a = player[color].get_action(state, api.Timer(args['time']))
        player[WHITE].update_move(a)
        player[BLACK].update_move(a)
        state = get_next_state(state, a, color)
        proc = SimpleStateProcessor(state)
        proc.process()
        color = get_oponent_color(color)
    if proc.get_winner() == WHITE:
        points[WHITE] += 1
    elif proc.get_winner() == BLACK:
        points[BLACK] += 1
    else:
        points[EMPTY] += 1
    pbar.update(i)
pbar.finish()

def fit_to(s, chars):
    s += ':'
    while len(s) < chars+1:
        s += ' '
    return s

print("RESULTS OF {} games:".format(args['games']))
total = points[WHITE] + points[BLACK] + points[EMPTY]
chars = max(len(algos[WHITE].__name__), len(algos[BLACK].__name__))
name_white = fit_to(algos[WHITE].__name__, chars)
name_black = fit_to(algos[BLACK].__name__, chars)
name_draws = fit_to("draws", chars)
print("(WHITE) {0} {1:.2f}%".format(name_white, 100*points[WHITE]/total))
print("(BLACK) {0} {1:.2f}%".format(name_black, 100*points[BLACK]/total))
print("{0} {1:.2f}%".format(name_draws, 100*points[EMPTY]/total))