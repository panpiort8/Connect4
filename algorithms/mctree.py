from algorithms import *
from environment import *
import random
import numpy as np

def check_if_terminal(state):
    proc = SimpleStateProcessor(state)
    proc.process()
    return proc.is_terminal(), proc.get_winner()

def get_reward(my_color, winner):
    if my_color == winner: return 1
    elif winner == EMPTY: return 0
    else: return -1


class RandomRolloutStrategy:
    def get_next_state(self, state, color):
        a = random.choice(get_legal_actions(state))
        return get_next_state(state, a, color)

class UCBTreeStrategy:
    def get_next_edge(self, node, factor):
        best_ucb = -INF
        best_nodes = []
        for a, son in node.sons.items():
            ucb = self.calc_ucb(son, node, factor)
            if ucb > best_ucb:
                best_nodes = [a]
                best_ucb = ucb
            elif ucb == best_ucb:
                best_nodes.append(a)
        return random.choice(best_nodes)

    def calc_ucb(self, node, parent, factor):
        if node.visits == 0:
            return factor*INF
        return node.total_reward/node.visits + \
               factor*np.sqrt(2*np.log(parent.visits)/node.visits)



class Node:
    def __init__(self, state, parent, color):
        self.size = 1
        self.total_reward = 0
        self.visits = 0
        self.state = state
        self.parent = parent
        self.color = color
        self.sons = None
        terminal, winner = check_if_terminal(state)
        self.terminal = terminal
        if winner is not None:
            self.winner = winner

    def generate_sons(self):
        self.sons = dict()
        for action in get_legal_actions(self.state):
            next_state = get_next_state(self.state, action, self.color)
            son = Node(next_state, self, get_oponent_color(self.color))
            self.sons[action] = son

    def update_size(self):
        self.size = 1
        for a, son in self.sons.items():
            self.size += son.size


class MCTreeSearch(api.Algorithm):
    def __init__(self, color, tree_strategy = UCBTreeStrategy(),
                 rollout_strategy = RandomRolloutStrategy(),
                 gamma=1.0, reuse = True, rollouts=1):
        super().__init__(color)
        self.tree_strategy = tree_strategy
        self.rollout_strategy = rollout_strategy
        self.gamma = gamma
        self.reuse = reuse
        self.rollouts = rollouts
        self.root = None

    def get_action(self, state, timer = Timer(2), **kwargs):
        if not self.reuse or self.root == None or self.root.state != state:
            self.root = Node(state, None, self.color)

        while not timer.is_over():
            node = self.selection()
            if not node.terminal and node.visits > 0:
                node.generate_sons()
                self.update_sizes(node)
                node = random.choice(list(node.sons.items()))[1]
            rewards = []
            for i in range(self.rollouts):
                rewards.append(self.rollout(node))
            self.backpropagate(node, np.average(rewards))

        a = self.tree_strategy.get_next_edge(self.root, 0)
        return a

    def selection(self):
        node = self.root
        while node.sons is not None:
            action = self.tree_strategy.get_next_edge(node, 1)
            node = node.sons[action]
        return node

    def rollout(self, node):
        if node.terminal:
            return get_reward(self.color, node.winner)
        state = node.state
        terminal = False
        # depth = 0
        color = self.color
        while not terminal:
            state = self.rollout_strategy.get_next_state(state, color)
            color = get_oponent_color(color)
            terminal, winner = check_if_terminal(state)
            # depth += 1
        # return get_reward(self.color, winner)*np.power(self.gamma, depth)
        return get_reward(self.color, winner)

    def backpropagate(self, node, reward):
        if node.color == self.color: turn = -1
        else: turn = 1
        while node is not None:
            node.visits += 1
            node.total_reward += turn*reward
            node = node.parent
            turn *= -1

    def update_sizes(self, node):
        while node is not None:
            node.update_size()
            node = node.parent


    def update_move(self, action):
        if self.root != None and self.root.sons != None:
            self.root = self.root.sons[action]