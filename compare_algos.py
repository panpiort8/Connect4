#!/usr/bin/env python3
import algorithms.api as api
import algorithms
import argparse
import sys
import environment as env
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
parser.add_argument('-w', '--white_algorithm', type=str, help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
parser.add_argument('-b', '--black_algorithm', type=str, help='algorithm to simulate (' + ','.join([name for name, cls in all_algos]) + ')', required = True)
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
time = args['time']
games = args['games']

points = dict()
points[env.WHITE] = 0
points[env.BLACK] = 0
points[env.EMPTY] = 0

print("Comparing {} as WHITE and {} as BLACK".format(algos[env.WHITE].__name__, algos[env.BLACK].__name__))
widgets = ["Games: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=games, widgets=widgets).start()
for i in range(games):
    state = env.get_initial_state()
    proc = env.StateProcessor()
    proc.process(state)
    color = env.WHITE
    while not proc.isTerminal():
        a = player[color].getAction(state, time)
        env.perform_action(state, a, color)
        proc.process(state)
        color = env.get_oponent_color(color)
    if proc.getTuplesNumber(4, env.WHITE) > 0:
        points[env.WHITE] += 1
    elif proc.getTuplesNumber(4, env.BLACK) > 0:
        points[env.BLACK] += 1
    else:
        points[env.EMPTY] += 1
    pbar.update(i)
pbar.finish()

def fit_to(s, chars):
    s += ':'
    while len(s) < chars+1:
        s += ' '
    return s

print("RESULTS OF {} games:".format(games))
total = points[env.WHITE] + points[env.BLACK] + points[env.EMPTY]
chars = max(len(algos[env.WHITE].__name__), len(algos[env.BLACK].__name__))
name_white = fit_to(algos[env.WHITE].__name__, chars)
name_black = fit_to(algos[env.BLACK].__name__, chars)
name_draws = fit_to("draws", chars)
print("{0} {1:.2f}%".format(name_white, 100*points[env.WHITE]/total))
print("{0} {1:.2f}%".format(name_black, 100*points[env.BLACK]/total))
print("{0} {1:.2f}%".format(name_draws, 100*points[env.EMPTY]/total))