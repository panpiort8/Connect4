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

class SimpleStateProcessor(api.StateProcessor):
    def process(self):
        state = [list(c) for c in self.state]
        full_colums = 0
        for c in state:
            l = len(c)
            if l == HEIGHT: full_colums += 1
            for i in range(HEIGHT-l):
                c.append(EMPTY)

        for iterator in [VertIterator, HorIterator, DiagLeftUpIterator, DiagRightUpIterator]:
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


class AlphaStateProcessor(SimpleStateProcessor):

    def process(self):
        super().process()
        if self.is_terminal():
            if self.winner == WHITE:
                self.value = 10000
            elif self.winner == BLACK:
                self.value = -10000
            else:
                self.value = 0
            return

        self.s = [list(c) for c in self.state]
        for c in self.s:
            while len(c) < HEIGHT:
                c.append(EMPTY)

        self.counts = dict()
        self.counts[WHITE] = [0, 0, 0, 0, 0]
        self.counts[BLACK] = [0, 0, 0, 0, 0]
        for iterator in [VertIterator, HorIterator, DiagRightUpIterator, DiagLeftUpIterator]:
            for color in (WHITE, BLACK):
                for w, h in iterator.start_positions():
                    back_empty = 0
                    l = 0
                    gaps = 0
                    while 0 <= w < WIDTH and 0 <= h < HEIGHT:
                        if self.s[w][h] == color:
                            l += 1
                        elif self.s[w][h] == EMPTY:
                            if l == 0:
                                back_empty += 1
                            else:
                                gaps += 1
                                l += 1
                        nw, nh = iterator.next(w, h)
                        if self.s[w][h] == get_oponent_color(color) or l == 4 or not (0 <= nw < WIDTH and 0 <= nh < HEIGHT):
                            if l == 4:
                                self.counts[color][4-gaps] += 1
                            elif l == 3 and back_empty > 0:
                                self.counts[color][3-gaps] += 1
                            elif l == 2 and back_empty > 1:
                                self.counts[color][2-gaps] += 1

                            if l == 4:
                                back_empty = 1
                            else:
                                back_empty = 0
                            gaps = 0
                            l = 0

                        w, h = iterator.next(w, h)

        weight2 = 1
        weight3 = 20
        white_points = weight2*self.counts[WHITE][2] + weight3*self.counts[WHITE][3]
        black_points = weight2*self.counts[BLACK][2] + weight3*self.counts[BLACK][3]
        self.value =  white_points - black_points

    def utility(self, my_color):
        return self.value if my_color == WHITE else -self.value
