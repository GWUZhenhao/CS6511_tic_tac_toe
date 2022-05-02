import time

import numpy as np
from unittest import TestCase
import utils as ut
import operation as op

class TTT_run():

    def __init__(self, board_size=10, target=5):
        self.game = ut.Game(board_size, target)
        self.gameId = 0  #  gameid 3657 zhenhao tianheng2
        self.teamId = 0  #  zhenhao  tianheng2 1336
    def get_state_board(self): # use board map to get state in narray
        key, value = op.get_board_map(self.gameId)
        for i, point in enumerate(key):
            self.game.current_state[point[0]][point[1]] = value[i]

    def get_turn(self):  # determine whether my turn to move
        moveIds, teamIds, symbols, moveXs, moveYs = op.get_moves(self.gameId, 1)
        if teamIds[-1] == self.teamId:
            return False
        else:
            return True

    def make_decision(self): #find best move in current state
        x,y = self.game.play_alpha_beta()
        return x,y

    def make_a_move(self,x,y):
        result = op.make_a_move(self.gameId,f"{x},{y}")
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
    #     st = time.time()
    #     score = self.game.evaluation_function(state_board)
    #     print('\n\nThe calculate time is {}'.format(time.time()-st))
    #     print('The evaluation score is {}.\n\n'.format(score))
    #     return score
        # assert False

