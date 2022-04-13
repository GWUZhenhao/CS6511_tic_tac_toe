import numpy as np

# Here is a way using Node class
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

# Another way just focus on the game itself. Don't use Node class
class Game:
    def __init__(self, board_size, target):

        # For current board state:
        # All the initial value is 0
        # Player 1 use 1
        # Player 2 use 2
        self.current_state = np.zeros([board_size, board_size], dtype='int8')
        self.board_size = board_size
        # The player 1 will go first
        self.player_turn = 1
        self.target = target

    def draw_board(self):
        print(self.current_state)

    # Determines if the made move is a legal move
    def is_valid(self, x, y):
        if self.current_state[x][y] != 0:
            return False
        return True

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # TODO: Check the game is end or not.
        # if the game is not end, return None
        return None

    def max_alpha_beta(self, alpha, beta):
        # Possible values for maxv are:
        # -10 - loss
        # 0  - a tie
        # 10  - win

        # Initialize max_V as -11 worse than the worse case
        max_V = -11
        px = None
        py = None

        result = self.is_end()

        if result == 1:
            return (-10, 0, 0)
        elif result == 2:
            return (10, 0, 0)
        elif result == 0:
            return (0, 0, 0)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == 0:
                    # On the empty field player 2 makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 2
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > max_V:
                        max_V = m
                        px = i
                        py = j

                    # Setting back the field to empty
                    self.current_state[i][j] = 0

                    # if max_V is bigger than current beta, we can prune. (No need check more children node)
                    if max_V >= beta:
                        return (max_V, px, py)

                    # if max_V is bigger than current alpha, update the alpha value
                    if max_V > alpha:
                        alpha = max_V

        return (max_V, px, py)

    def min_alpha_beta(self, alpha, beta):

        # Initialize min_V as 11 better than the better case
        min_V = 11

        qx = None
        qy = None

        result = self.is_end()

        if result == 1:
            return (-10, 0, 0)
        elif result == 2:
            return (10, 0, 0)
        elif result == 0:
            return (0, 0, 0)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == 0:
                    # On the empty field player 1 makes a move and calls Max
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 1
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < min_V:
                        min_V = m
                        qx = i
                        qy = j

                    # Setting back the field to empty
                    self.current_state[i][j] = 0

                    # if min_V is smaller than current alpha, we can prune. (No need check more children node)
                    if min_V <= alpha:
                        return (min_V, qx, qy)

                    # if min_V is smaller than current beta, update the beta value
                    if min_V < beta:
                        beta = min_V

        return (min_V, qx, qy)

    def play_alpha_beta(self):
        while True:
            self.result = self.is_end()

            if self.result != None:
                if self.result == 1:
                    print('The winner is player 1!')
                elif self.result == 2:
                    print('The winner is player 2!')
                elif self.result == 0:
                    print("It's a tie!")

                return

            if self.player_turn == 1:
                # TODO: The player 1 will play
                (m, qx, qy) = self.min_alpha_beta(-11, 11)
                print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                self.player_turn = 2

            else:
                (m, px, py) = self.max_alpha_beta(-11, 11)
                self.current_state[px][py] = 2
                self.player_turn = 1

