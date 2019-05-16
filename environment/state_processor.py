from environment import *
from algorithms import api

class Iterator:
    @staticmethod
    def start_positions():
        pass
    @staticmethod
    def next(w, h):
        return None

class VertIterator(Iterator):
    @staticmethod
    def start_positions():
        return [(w, 0) for w in range(WIDTH)]
    @staticmethod
    def next(w, h):
        return w, h+1

class HorIterator(Iterator):
    @staticmethod
    def start_positions():
        return [(0, h) for h in range(HEIGHT)]
    @staticmethod
    def next(w, h):
        return w + 1, h

class DiagRightUpIterator(Iterator):
    @staticmethod
    def start_positions():
        return [(w, HEIGHT-1) for w in range(WIDTH)]\
               +[(WIDTH-1, h) for h in range(HEIGHT-1)]
    @staticmethod
    def next(w, h):
        return w - 1, h - 1

class DiagLeftUpIterator(Iterator):
    @staticmethod
    def start_positions():
        return [(w, HEIGHT-1) for w in range(WIDTH)]\
               +[(0, h) for h in range(HEIGHT-1)]
    @staticmethod
    def next(w, h):
        return w + 1, h - 1

class AlphaStateProcessor:
    def _get_initial_mapping(self):
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
        self.total[WHITE] = self._get_initial_mapping()
        self.total[BLACK] = self._get_initial_mapping()
        for iterator, sumDict in zip(
                [VertIterator, HorIterator, DiagRightUpIterator, DiagLeftUpIterator],
                [self.vertical, self.horizontal, self.diagRightUp, self.diagLeftUp]):
            for color in (WHITE, BLACK):
                sumDict[color] = self._get_initial_mapping()
                for w, h in iterator.start_positions():
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

class SimpleStateProcessor(api.StateProcessor):
    def process(self):
        state = [list(c) for c in self.state]
        full_colums = 0
        for c in state:
            l = len(c)
            if l == HEIGHT: full_colums += 1
            for i in range(HEIGHT-l):
                c.append(EMPTY)

        for iterator in [VertIterator, HorIterator, DiagLeftUpIterator, DiagLeftUpIterator]:
            for w, h in iterator.start_positions():
                black = 0
                white = 0
                while 0 <= w < WIDTH and 0 <= h < HEIGHT:
                    if state[w][h] == WHITE:
                        white += 1
                        black = 0
                    elif state[w][h] == BLACK:
                        black += 1
                        white = 0
                    else:
                        black = 0
                        white = 0
                    if black >= 4:
                        self.terminal = True
                        self.winner = BLACK
                        return
                    if white >= 4:
                        self.terminal = True
                        self.winner = WHITE
                        return
                    w, h = iterator.next(w, h)
        self.terminal = full_colums == 7
        self.winner = EMPTY
