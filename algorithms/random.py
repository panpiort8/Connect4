from algorithms import api
import environment as env
import random

class RandomAlgorithm(api.Algorithm):
    def _get_action(self, state, timer, max_depth):
        return random.choice(env.get_legal_actions(state))