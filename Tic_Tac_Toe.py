
player1 = 1
player2 = 2

max_depth = 5
max_node = 20

num = 10
six = 9
five = 8
s_five = 7
four = 6
s_four = 5
three = 4
s_three = 3
two = 2
s_two = 1

score_6 = 500000
socre_5, s_five, socre_4, socre_s_4 = 100000, 50000, 10000, 1000
socre_3, socre_s_3, socre_2, socre_s_2 = 100, 10, 8, 2

class tic_tac_toe():
    def __init__(self, n, m):
        self.len = n
        self.target = m
        self.record = [[[0, 0, 0, 0] for i in range(self.len)] for y in range(self.len)]
        self.count = [[0 for i in range(num)] for i in range(2)]

    def reset(self):
        self.record = [[[0, 0, 0, 0] for i in range(self.len)] for y in range(self.len)]
        self.count = [[0 for i in range(num)] for i in range(2)]

    def check_win(self, board, turn):
        self.reset()
        if turn == player1:
            ai = 1
            opponent = 2
        else:
            ai = 2
            opponent = 1

        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == ai:
                    self.evaluate_one(board, x, y, ai, opponent)
                elif board[y][x] == opponent:
                    self.evaluate_one(board, x, y, opponent, ai)
        ai_count = self.count[ai - 1]
        return ai_count[self.target*2-2] > 0

    def evaluate_score(self, board, x, y, ai, opponent):  

        self.count = [[0 for i in range(num)] for i in range(2)]

        board[y][x] = ai
        self.evaluate_one(board, x, y, ai, opponent, self.count[ai - 1])
        board[y][x] = opponent
        self.evaluate_one(board, x, y, opponent, ai, self.count[opponent - 1])
        board[y][x] = 0

        ai_score = self.get_score(self.count[ai - 1])
        opponent_score = self.get_score(self.count[opponent - 1])

        return (ai_score, opponent_score)

    def neighbor(self, board, x, y, r):
        start_x, end_x = (x - r), (x + r)
        start_y, end_y = (y - r), (y + r)

        for i in range(start_y, end_y + 1):
            for j in range(start_x, end_x + 1):
                if i >= 0 and i < self.len and j >= 0 and j < self.len:
                    if board[i][j] != 0:
                        return True
        return False

    def heuristic(self, board, turn):
        five = []
        ai_four, op_four = [], []
        ai_s_four, op_s_four = [], []
        if turn == player1:
            ai = 1
            opponent = 2
        else:
            ai = 2
            opponent = 1

        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0 and self.neighbor(board, x, y, 1):
                    ai_score, opponent_score = self.evaluate_score(board, x, y, ai, opponent)
                    point = (max(ai_score, opponent_score), x, y)

                    if ai_score >= socre_5 or opponent_score >= socre_5:
                        five.append(point)
                    elif ai_score >= socre_4:
                        ai_four.append(point)
                    elif opponent_score >= socre_4:
                        op_four.append(point)
                    elif ai_score >= socre_s_4:
                        ai_s_four.append(point)
                    elif opponent_score >= socre_s_4:
                        op_s_four.append(point)

                    moves.append(point)

        if len(five) > 0:
            return five

        if len(ai_four) > 0:
            return ai_four

        if len(op_four) > 0:
            if len(ai_s_four) == 0:
                return op_four
            else:
                return op_four + ai_s_four

        moves.sort(reverse=True)

        if max_depth > 2 and len(moves) > max_node:
            moves = moves[:max_node]
        return moves

    def alpha_beta(self, board, turn, depth, alpha = -2**31, beta=2**31-1):
        score = self.evaluate(board, turn)
        if depth <= 0 or abs(score) >= socre_5:
            return score

        moves = self.heuristic(board, turn)
        choice = None
        self.alpha += len(moves)

        if len(moves) == 0:
            return score

        for point, x, y in moves:
            board[y][x] = turn

            if turn == player1:
                op_turn = player2
            else:
                op_turn = player1

            score = - self.alpha_beta(board, op_turn, depth - 1, -beta, -alpha)

            board[y][x] = 0
            self.belta += 1

            if score > alpha:
                alpha = score
                choice = (x, y)
                if alpha >= beta:
                    break

        if depth == max_depth and choice:
            self.choice = choice

        return alpha

    def search(self, board, turn):
        self.alpha = 0
        self.belta = 0
        self.choice = (0,0)
        self.alpha_beta(board, turn, max_depth)
        return self.choice

    def get_score(self, count):
        score = 0
        if count[five] > 0:
            return socre_5

        if count[four] > 0:
            return socre_4

        if count[s_four] > 1:
            score += count[s_four] * socre_s_4
        elif count[s_four] > 0 and count[three] > 0:
            score += count[s_four] * socre_s_4
        elif count[s_four] > 0:
            score += socre_3

        if count[three] > 1:
            score += 5 * socre_3
        elif count[three] > 0:
            score += socre_3

        if count[s_three] > 0:
            score += count[s_three] * socre_s_3
        if count[two] > 0:
            score += count[two] * socre_2
        if count[s_two] > 0:
            score += count[s_two] * socre_s_2

        return score

    def evaluate(self, board, turn):
        self.reset()

        if turn == player1:
            ai = 1
            opponent = 2
        else:
            ai = 2
            opponent = 1

        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == ai:
                    self.evaluate_one(board, x, y, ai, opponent)
                elif board[y][x] == opponent:
                    self.evaluate_one(board, x, y, opponent, ai)

        ai_count = self.count[ai - 1]
        opponent_count = self.count[opponent - 1]
        ai_score = self.get_score(ai_count)
        opponent_score = self.get_score(opponent_count)
        return ai_score - opponent_score

    def evaluate_one(self, board, x, y, ai, opponent, count=None):
        direction = [(1, 0), (0, 1), (1, 1), (1, -1)]  
        record = True
        if count is None:
            count = self.count[ai - 1]
            record = False
        for i in range(4):
            if self.record[y][x][i] == 0 or record:
                self.board_type(board, x, y, i, direction[i], ai, opponent, count)

    def set_record(self, x, y, left, right, dir_index, direction):
        x += (-5 + left) * direction[0]
        y += (-5 + left) * direction[1]
        for i in range(left, right + 1):
            x += direction[0]
            y += direction[1]
            self.record[y][x][dir_index] = 1

    def board_type(self, board, x, y, dir_index, dir, ai, opponent, count):

        left, right = 4, 4
        line = [0 for i in range(self.target*2-1)]

        xx = x + (-5 * dir[0])
        yy = y + (-5 * dir[1])
        for i in range(self.target*2-1):
            xx += dir[0]
            yy += dir[1]
            if (xx < 0 or xx >= self.len or
                    yy < 0 or yy >= self.len):
                line[i] = opponent
            else:
                line[i] = board[yy][xx]

        while right < 8:
            if line[right + 1] != ai:
                break
            right += 1
        while left > 0:
            if line[left - 1] != ai:
                break
            left -= 1

        left_range, right_range = left, right
        while right_range < 8:
            if line[right_range + 1] == opponent:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range - 1] == opponent:
                break
            left_range -= 1

        chess_range = right_range - left_range + 1
        if chess_range < 5:
            self.set_record(x, y, left_range, right_range, dir_index, dir)
            return 0

        self.set_record(x, y, left, right, dir_index, dir)

        m_range = right - left + 1

        if m_range >= 5:
            count[five] += 1

        if m_range == 4:
            left_empty = right_empty = False
            if line[left - 1] == 0:
                left_empty = True
            if line[right + 1] == 0:
                right_empty = True
            if left_empty and right_empty:
                count[four] += 1
            elif left_empty or right_empty:
                count[s_four] += 1

        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left - 1] == 0:
                if line[left - 2] == ai:
                    self.set_record(x, y, left - 2, left - 1, dir_index, dir)
                    count[s_four] += 1
                    left_four = True
                left_empty = True

            if line[right + 1] == 0:
                if line[right + 2] == ai:
                    self.set_record(x, y, right + 1, right + 2, dir_index, dir)
                    count[s_four] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:
                    count[three] += 1
                else:
                    count[s_three] += 1
            elif left_empty or right_empty:
                count[s_three] += 1

        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left - 1] == 0:
                if line[left - 2] == ai:
                    self.set_record(x, y, left - 2, left - 1, dir_index, dir)
                    if line[left - 3] == 0:
                        if line[right + 1] == 0:
                            count[three] += 1
                        else:
                            count[s_three] += 1
                        left_three = True
                    elif line[left - 3] == opponent:
                        if line[right + 1] == 0:
                            count[s_three] += 1
                            left_three = True

                left_empty = True

            if line[right + 1] == 0:
                if line[right + 2] == ai:
                    if line[right + 3] == ai:
                        self.set_record(x, y, right + 1, right + 2, dir_index, dir)
                        count[s_four] += 1
                        right_three = True
                    elif line[right + 3] == 0:
                        if left_empty:
                            count[three] += 1
                        else:
                            count[s_three] += 1
                        right_three = True
                    elif left_empty:
                        count[s_three] += 1
                        right_three = True

                right_empty = True

            if left_three or right_three:
                pass
            elif left_empty and right_empty:
                count[two] += 1
            elif left_empty or right_empty:
                count[s_two] += 1

        if m_range == 1:
            left_empty = right_empty = False
            if line[left - 1] == 0:
                if line[left - 2] == ai:
                    if line[left - 3] == 0:
                        if line[right + 1] == opponent:
                            count[s_two] += 1
                left_empty = True

            if line[right + 1] == 0:
                if line[right + 2] == ai:
                    if line[right + 3] == 0:
                        if left_empty:
                            count[two] += 1
                        else:
                            count[s_two] += 1
                elif line[right + 2] == 0:
                    if line[right + 3] == ai and line[right + 4] == 0:
                        count[two] += 1
