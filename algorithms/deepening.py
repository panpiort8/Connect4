from algorithms import *
import environment as env

class TransitionTable:
    def __init__(self, size):
        self.size = size
        self.cache = [(None, None) for i in range(self.size)]

    def get(self, key):
        ent, val = self.cache[hash(key)%self.size]
        if ent == key: return val
        else: return None

    def put(self, key, val):
        self.cache[hash(key)%self.size] = (key, val)

class DeepeningAlgorithm(AlphaBetaAlgorithm):
    def __init__(self, color):
        super().__init__(color)
        self.table = TransitionTable(50000)

    def get_fresh_dict(self):
        d = dict()
        for i in range(env.WIDTH):
            d[i] = 0
        return d

    def _get_action(self, state, timer, max_depth):
        depth = 1
        a = -1
        self.nodes = 0
        while not timer.is_over():
            self.max_depth = depth
            a, v = self.alphabeta(state, depth, -env.INF, env.INF, True, timer)
            depth += 1
        return a

    def alphabeta(self, state, depth, alpha, beta, max_player, timer):
        state_proc = env.AlphaStateProcessor()
        state_proc.process(state)
        self.nodes += 1
        if depth == 0 or state_proc.isTerminal() or timer.is_over():
            return -1, self.utility(state_proc, depth+1)

        actions = self.table.get(state)
        if actions is None:
            actions = self.get_fresh_dict()
        if max_player:
            max_act = -1
            for a, v in reversed(sorted(actions.items(), key= lambda kv: kv[1])):
                if len(state[a]) >= 6:
                    continue
                next_state = env.get_next_state(state, a, self.color)
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, False, timer)
                actions[a] = val
                if alpha < val:
                    alpha = val
                    max_act = a
                if alpha >= beta:
                    break
            self.table.put(state, actions)
            return max_act, alpha
        else:
            min_act = -1
            for a, v in sorted(actions.items(), key=lambda kv: kv[1]):
                if len(state[a]) >= 6:
                    continue
                next_state = env.get_next_state(state, a, env.get_oponent_color(self.color))
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, True, timer)
                actions[a] = val
                if beta > val:
                    beta = val
                    min_act = a
                if alpha >= beta:
                    break
            self.table.put(state, actions)
            return min_act, beta