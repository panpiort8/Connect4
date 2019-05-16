import time

class Timer:
    def __init__(self, t):
        self.start = time.time()
        self.time = t

    def isOver(self):
        return time.time()-self.start >= self.time

class Algorithm:
    def __init__(self, color):
        self.color = color
        self.nodes = 0

    def getAction(self, state, timer = Timer(1), max_depth = 4):
        return self._getAction(state, timer, max_depth)

    def _getAction(self, state, timer, max_depth):
        pass