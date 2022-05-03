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

    def neighbor(self, board, x, y, r):
        start_x, end_x = (x - r), (x + r)
        start_y, end_y = (y - r), (y + r)

        for i in range(start_y, end_y + 1):
            for j in range(start_x, end_x + 1):
                if i >= 0 and i < self.board_size and j >= 0 and j < self.board_size:
                    if board[i][j] != 0:
                        return True
        return False

    def draw_board(self):
        print(self.current_state)

    # Determines if the made move is a legal move
    def is_valid(self, x, y):
        if self.current_state[x][y] != 0:
            return False
        return True

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # Vertical win
        for i in range(self.board_size):
            for j in range(self.board_size - self.target + 1):
                for k in range(self.target - 2):
                    if (self.current_state[j + k][i] == 0 or self.current_state[j + k][i] != self.current_state[j + k + 1][i]):
                        break
                    elif k == (self.target - 2):
                        return self.current_state[j][i]

        # Horizontal win
        for i in range(self.board_size):
            for j in range(self.board_size - self.target + 1):
                for k in range(self.target - 2):
                    if (self.current_state[i][j + k] == 0 or self.current_state[i][j + k] != self.current_state[i][j + k + 1]):
                        break
                    elif k == (j + self.target - 2):
                        return self.current_state[i][j]

        # Main diagonal win
        for i in range(self.board_size - self.target + 1):
            for j in range(self.board_size - self.target + 1):
                for k in range(self.target - 2):
                    if (self.current_state[i + k][j + k] == 0 or self.current_state[i + k][j + k] != self.current_state[i + k + 1][j + k + 1]):
                        break
                    elif k == (self.target - 2):
                        return self.current_state[i][j]

        # Second diagonal win
        for i in range(self.board_size - self.target + 1):
            for j in range(self.target - 1, self.board_size):
                for k in range(self.target - 2):
                    if (self.current_state[i + k][j -k] == 0 or self.current_state[i + k][j - k] != self.current_state[i + k + 1][j - k - 1]):
                        break
                    elif k == (self.target - 2):
                        return self.current_state[i][j]

        # if the game is not end, return None
        return None

    def max_alpha_beta(self, alpha, beta, explore_layer, max_explore_layer):
        # Possible values for maxv are:
        # -10 - loss
        # 0  - a tie
        # 10  - win

        # Initialize max_V as -11 worse than the worse case
        # a = pow(10, 10)
        a = 10
        ##max_V = -11
        max_V = -a-1
        px = None
        py = None

        result = self.is_end()

        if result == 1:
            return (-a, 0, 0)
        elif result == 2:
            return (a, 0, 0)
        elif result == 0:
            return (0, 0, 0)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == 0 and self.neighbor(self.current_state,i,j,1):
                    # On the empty field player 2 makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 2
                    #print("consider 2 x,y:", i, j)
                    explore_layer += 1
                    if explore_layer >= max_explore_layer:
                        m = self.evaluation_function(self.current_state)
                        # print("MAXeva: x,y", m, i, j)
                    else:
                        (m, min_i, in_j) = self.min_alpha_beta(alpha, beta, explore_layer, max_explore_layer)
                        # print("MAX from minab:", m, i, j)
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

    def min_alpha_beta(self, alpha, beta, explore_layer,max_explore_layer):

        # Initialize min_V as 11 better than the better case
        # a = pow(10, 10)
        a = 10
        #min_V = 11
        min_V = a+1

        qx = None
        qy = None

        result = self.is_end()

        if result == 1:
            return (-a, 0, 0)
        elif result == 2:
            return (a, 0, 0)
        elif result == 0:
            return (0, 0, 0)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == 0 and self.neighbor(self.current_state,i,j,1):
                    # On the empty field player 1 makes a move and calls Max
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 1
                    # print("consider 1 x,y:", i,j)
                    explore_layer += 1
                    if explore_layer >= max_explore_layer:
                        m = self.evaluation_function(self.current_state)
                        # print("mineva: x,y",m,i,j)
                        # print("m of evalu func", m)
                    else:
                        (m, min_i, in_j) = self.max_alpha_beta(alpha, beta, explore_layer, max_explore_layer)
                        # print("min from maxab:",m,i,j)
                        # print("m of max:",m)
                    if m < min_V:
                        min_V = m
                        qx = i
                        qy = j
                        # print("m<minv:m ,i,j", m,i,j)

                    # Setting back the field to empty
                    self.current_state[i][j] = 0

                    # if min_V is smaller than current alpha, we can prune. (No need check more children node)
                    if min_V <= alpha:
                        # print("m<=alpha")
                        return (min_V, qx, qy)

                    # if min_V is smaller than current beta, update the beta value
                    if min_V < beta:
                        # print("minv<=beta",min_V)
                        beta = min_V

        return (min_V, qx, qy)

    def evaluation_function(self, state_board):
        # store the number of each chain for each player
        nums_chain_1 = np.zeros(self.target)
        nums_chain_2 = np.zeros(self.target)

        # traverse the board
        # lateral row
        for i in range(0, self.board_size):
            for j in range(0, self.board_size - self.target):
                ROI = state_board[i][j:j+self.target]
                # if this ROI only has 1
                if np.sum(np.unique(ROI)) == 1:
                    # Update the nums_chain_1 base on the consecutive number
                    consecutive_number = np.sum(ROI == 1)
                    nums_chain_1[consecutive_number-1] += 1
                if np.sum(np.unique(ROI)) == 2:
                    # Update the nums_chain_2 base on the consecutive number
                    consecutive_number = np.sum(ROI == 2)
                    nums_chain_2[consecutive_number - 1] += 1
                # other condition will continue
                else:
                    continue
        # vertical: just transpose the matrix, same as the lateral one
        for i in range(0, self.board_size - self.target):
            for j in range(0, self.board_size):
                # transpose the matrix here
                ROI = state_board.T[i][j:j + self.target]
                # if this ROI only has 1
                if np.sum(np.unique(ROI)) == 1:
                    # Update the nums_chain_1 base on the consecutive number
                    consecutive_number = np.sum(ROI == 1)
                    nums_chain_1[consecutive_number - 1] += 1
                if np.sum(np.unique(ROI)) == 2:
                    # Update the nums_chain_2 base on the consecutive number
                    consecutive_number = np.sum(ROI == 2)
                    nums_chain_2[consecutive_number - 1] += 1
                # other condition will continue
                else:
                    continue
        # diagonal: The way to extract the ROI is different. Just pick the diagonal for the matrix
        for i in range(self.target - self.board_size, self.board_size - self.target+1):
            dia = state_board.diagonal(offset=i)
            for j in range(len(dia)-self.target+1):
                ROI = dia[j:j+self.target]
                # if this ROI only has 1
                if np.sum(np.unique(ROI)) == 1:
                    # Update the nums_chain_1 base on the consecutive number
                    consecutive_number = np.sum(ROI == 1)
                    nums_chain_1[consecutive_number - 1] += 1
                if np.sum(np.unique(ROI)) == 2:
                    # Update the nums_chain_2 base on the consecutive number
                    consecutive_number = np.sum(ROI == 2)
                    nums_chain_2[consecutive_number - 1] += 1
                # other condition will continue
                else:
                    continue
        # anti-diagonal: compared to the diagonal, just horizontal flip the matrix
        for i in range(self.target - self.board_size, self.board_size - self.target + 1):
            dia = np.fliplr(state_board).diagonal(offset=i)
            for j in range(len(dia) - self.target + 1):
                ROI = dia[j:j + self.target]
                # if this ROI only has 1
                if np.sum(np.unique(ROI)) == 1:
                    # Update the nums_chain_1 base on the consecutive number
                    consecutive_number = np.sum(ROI == 1)
                    nums_chain_1[consecutive_number - 1] += 1
                if np.sum(np.unique(ROI)) == 2:
                    # Update the nums_chain_2 base on the consecutive number
                    consecutive_number = np.sum(ROI == 2)
                    nums_chain_2[consecutive_number - 1] += 1
                # other condition will continue
                else:
                    continue


        # Calculate the score based on the nums_chain_1 and nums_chain_2
        score_1 = np.sum([num * pow(10, index) for index, num in enumerate(nums_chain_1)])
        score_2 = np.sum([num * pow(10, index) for index, num in enumerate(nums_chain_2)])
        #
        final_score = (score_1 - score_2)/(score_1 + score_2) *10
        # final_score = score_1 -score_2
        return final_score

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
            a = 10
            # a = pow(10,10)
            if self.player_turn == 1:
                # TODO: The player 1 will play

                (m, qx, qy) = self.min_alpha_beta(-a-1, a+1, 0, 10000)
                print('Recommended move: X = {}, Y = {}'.format(qx+1, qy+1))
                return qx+1,qy+1
                self.player_turn = 2

            else:

                (m, px, py) = self.max_alpha_beta(-a-1, a+1, 0, 10000)
                print('Recommended move: X = {}, Y = {}'.format(px+1, py+1))
                return px+1,py+1
                self.current_state[px][py] = 2
                self.player_turn = 1

