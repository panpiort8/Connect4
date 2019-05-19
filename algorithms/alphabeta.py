from algorithms import api
import environment as env

class AlphaBetaAlgorithm(api.Algorithm):

    def _get_action(self, state, timer, max_depth):
        self.nodes = 0
        self.max_depth = max_depth
        a, v = self.alphabeta(state, max_depth, -env.INF, env.INF, True, timer)
        return a

    def alphabeta(self, state, depth, alpha, beta, max_player, timer):
        self.nodes += 1
        state_proc = env.AlphaStateProcessor()
        state_proc.process(state)
        if depth == 0 or state_proc.isTerminal() or timer.is_over():
            return -1, self.utility(state_proc, depth+1)

        if max_player:
            max_act = -1
            for a in env.get_legal_actions(state):
                next_state = env.get_next_state(state, a, self.color)
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, False, timer)
                if alpha < val:
                    alpha = val
                    max_act = a
                if alpha >= beta:
                    break
            return max_act, alpha
        else:
            min_act = -1
            for a in env.get_legal_actions(state):
                next_state = env.get_next_state(state, a, env.get_oponent_color(self.color))
                _, val = self.alphabeta(next_state, depth - 1, alpha, beta, True, timer)
                if beta > val:
                    beta = val
                    min_act = a
                if alpha >= beta:
                    break
            return min_act, beta
