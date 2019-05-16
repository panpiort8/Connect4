from environment import *

class VertIterator:
    @staticmethod
    def startPositions():
        return [(w, 0) for w in range(WIDTH)]
    @staticmethod
    def next(w, h):
        return w, h+1

class HorIterator:
    @staticmethod
    def startPositions():
        return [(0, h) for h in range(HEIGHT)]
    @staticmethod
    def next(w, h):
        return w + 1, h

class DiagRightUpIterator:
    @staticmethod
    def startPositions():
        return [(w, HEIGHT-1) for w in range(WIDTH)]\
               +[(WIDTH-1, h) for h in range(HEIGHT-1)]
    @staticmethod
    def next(w, h):
        return w - 1, h - 1

class DiagLeftUpIterator:
    @staticmethod
    def startPositions():
        return [(w, HEIGHT-1) for w in range(WIDTH)]\
               +[(0, h) for h in range(HEIGHT-1)]
    @staticmethod
    def next(w, h):
        return w + 1, h - 1

class StateProcessor:
    def _getInitialMapping(self):
        return [0, 0, 0, 0, 0, 0, 0, 0]

    def process(self, state):
        self.s = [list(c) for c in state]
        self.full = len(get_legal_actions(state)) == 0
        for c in self.s:
            while len(c) < HEIGHT:
                c.append(EMPTY)

        self.vertical = dict()
        self.horizontal = dict()
        self.diagRightUp = dict()
        self.diagLeftUp = dict()
        self.total = dict()
        self.total[WHITE] = self._getInitialMapping()
        self.total[BLACK] = self._getInitialMapping()
        for iterator, sumDict in zip(
                [VertIterator, HorIterator, DiagRightUpIterator, DiagLeftUpIterator],
                [self.vertical, self.horizontal, self.diagRightUp, self.diagLeftUp]):
            for color in (WHITE, BLACK):
                sumDict[color] = self._getInitialMapping()
                for w, h in iterator.startPositions():
                    sum = 0
                    while 0 <= w < WIDTH and 0 <= h < HEIGHT:
                        if self.s[w][h] == color:
                            sum += 1
                        else:
                            sum = 0
                        sumDict[color][sum] += 1
                        self.total[color][sum] += 1
                        w, h = iterator.next(w, h)

    def isTerminal(self):
        return self.getTuplesNumber(4, WHITE) + self.getTuplesNumber(4, BLACK) > 0 or self.full

    def getTuplesNumber(self, k, color):
        return self.total[color][k]