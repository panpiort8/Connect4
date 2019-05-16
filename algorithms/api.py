import time

class Timer:
    def __init__(self, t):
        self.start = time.time()
        self.time = t

    def is_over(self):
        return time.time()-self.start >= self.time


class Algorithm:
    def __init__(self, color):
        self.color = color
        self.nodes = 0

    def get_action(self, state, timer, max_depth):
        return None

    def update_move(self, action):
        pass

class StateProcessor:
    def __init__(self, state):
        self.state = state

    def process(self):
        pass

    def is_terminal(self):
        return self.terminal

    def get_winner(self):
        return self.winner
