from algorithms import *
from environment import *
import sys
import random

class PlayerPseudoAlgorithm(Algorithm):
    def get_action(self, state, timer, max_depth=None):
        c = -1
        legal = get_legal_actions(state)
        while c-1 not in legal:
            printf("type number of column: ")
            sys.stdout.flush()
            c = int(sys.stdin.read(2))
        return c-1