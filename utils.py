import numpy as np

class Node:


    def __init__(self, state_board=None, agent = None, value=None):
        self.agent = agent
        self.state_board = state_board
        self.value = value
        self.parent = None
        self.children = []
        self.terminal = self.check_terminal()

        self.alpha = -100000
        self.beta = 100000

    def check_terminal(self):
        # TODO: If the board have no place for chess, return True
        return False

    @classmethod
    def calculate_value(self, node):
        if node.terminal == True:
            # TODO: For the full chess board, calculate the value
            node.value = 0
            return node.value

        if node.agent == 'Max':
            node.value = Node.max_value(node)
            return node.value

        if node.agent == 'Min':
            Node.min_value(node)

    @classmethod
    def max_value(self, node):
        # TODO: alpha, beta need to be updated
        v = -100000
        for successor in node.children:
            v = np.max(v, Node.calculate_value(successor))
            if v > successor.beta:
                return v
            successor.alpha = np.max(successor.alpha, v)
        return v

    @classmethod
    def min_value(self, node):
        # TODO: alpha, beta need to be updated
        v = -100000
        for successor in node.children:
            v = np.max(v, Node.calculate_value(node))
            if v <= successor.alpha:
                return v
            successor.beta = np.min(successor.beta, v)
        return v


node = Node(agent='Max')
Node.calculate_value(node)