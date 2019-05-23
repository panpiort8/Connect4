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

class AlphaBetaAlgorithm(Algorithm):
    def __init__(self, color, **kwargs):
        super().__init__(color)
        self.moving_order = TransitionTable(50000)
        self.proc_state_table = TransitionTable(50000)

    def get_fresh_dict(self):
        d = dict()
        for i in range(env.WIDTH):
            d[i] = 0
        return d

    def get_action(self, state, timer = Timer(2), **kwargs):
        depth = 1
        a = -1
        self.nodes = 0
        while not timer.is_over():
            try:
                a, n = self.alphabeta(state, depth, -env.INF, env.INF, True, timer)
            except:
                # print('Nodes visited:', self.nodes)
                return a
            depth += 1
        # print('Nodes visited:', self.nodes)
        return a

    def alphabeta(self, state, depth, alpha, beta, max_player, timer):
        state_proc = self.proc_state_table.get(state)
        if state_proc is None:
            state_proc = env.AlphaStateProcessor(state)
            state_proc.process()
            self.proc_state_table.put(state, state_proc)
            self.nodes += 1

        if timer.is_over():
            raise Exception('time is over!')

        if depth == 0 or state_proc.is_terminal():
            return -1, state_proc.utility(self.color)

        moving_order = self.moving_order.get(state)
        if moving_order is None:
            moving_order = self.get_fresh_dict()

        if max_player:
            max_act = -1
            for a, v in reversed(sorted(moving_order.items(), key= lambda kv: kv[1])):
                if len(state[a]) >= 6:
                    continue
                next_state = env.get_next_state(state, a, self.color)
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, False, timer)
                moving_order[a] = val
                if alpha < val:
                    alpha = val
                    max_act = a
                if alpha >= beta:
                    break
            self.moving_order.put(state, moving_order)
            return max_act, alpha
        else:
            min_act = -1
            for a, v in sorted(moving_order.items(), key=lambda kv: kv[1]):
                if len(state[a]) >= 6:
                    continue
                next_state = env.get_next_state(state, a, env.get_oponent_color(self.color))
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, True, timer)
                moving_order[a] = val
                if beta > val:
                    beta = val
                    min_act = a
                if alpha >= beta:
                    break
            self.moving_order.put(state, moving_order)
            return min_act, beta