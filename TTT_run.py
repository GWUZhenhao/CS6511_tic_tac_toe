import time

import numpy as np
from unittest import TestCase
#import utils as ut
import operation as op
from Tic_Tac_Toe import tic_tac_toe

class TTT_run():

    def __init__(self, board_size=12, target=6):
        self.game = tic_tac_toe(board_size, target)
        self.gameId = 0  #  gameid 3657 zhenhao tianheng2
        self.teamId = 0  #  zhenhao  tianheng2 1336
        self.op = 0
        self.board_size = board_size
        self.target = target
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]

    def get_state_board(self): # use board map to get state in narray
        key, value = self.op.get_board_map(self.gameId)
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        for i, point in enumerate(key):
            self.board[point[0]][point[1]] = value[i]

    def first_step(self):
        a = int(self.board_size / 2)
        self.op.make_a_move(self.gameId, f"{a},{a}")

    def get_turn(self):  # determine whether my turn to move
        if not self.op.get_moves(self.gameId, '1'):
            self.first_step()
            #print("if not")
            return False
        moveIds, teamIds, symbols, moveXs, moveYs = self.op.get_moves(self.gameId, '1')
        if teamIds[0] == self.teamId:
            #print("teamid:",teamIds)
            return False
        else:
            return True

    def make_decision(self): #find best move in current state
        turn = 1
        x,y = self.game.search(self.board, turn)
        return x,y

    def make_a_move(self,x,y):
        result = self.op.make_a_move(self.gameId,f"{x},{y}")
        return result



    # def test_evaluation_function(self):
    #     state_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    #                             [2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 1, 1, 1, 0, 2, 2, 2],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='int8')
    #
    #     score = self.game.evaluation_function(state_board)
    #
    #     print('The evaluation score is {}.\n\n'.format(score))
    #     return score
        # assert False
#
run = TTT_run()
run.teamId = '1304'  #1304
run.gameId = '3682'
run.op = op.operation("1304")
while True:
    if run.get_turn():
        st = time.time()
        print("start thinking")
        run.get_state_board()
        x,y = run.make_decision()
        result=run.make_a_move(x,y)
        print("result",result)
        print('The calculate time is {}'.format(time.time() - st))
        for i in run.board:
            print(i)
        time.sleep(1)
    else:
        print("it is not team turn")
        time.sleep(1)
