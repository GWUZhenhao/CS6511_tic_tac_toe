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
        self.op = 0
    def get_state_board(self): # use board map to get state in narray
        key, value = self.op.get_board_map(self.gameId)
        for i, point in enumerate(key):
            self.game.current_state[point[0]][point[1]] = value[i]

    def first_step(self):
        self.make_a_move(int(self.board_size/2),int(self.board_size/2))

    def get_turn(self):  # determine whether my turn to move
        if not self.op.get_moves(self.gameId, '2'):
            self.first_step()
            return False
        moveIds, teamIds, symbols, moveXs, moveYs = self.op.get_moves(self.gameId, '2')
        if teamIds[0] == self.teamId:
            return False
        else:
            return True

    def make_decision(self): #find best move in current state
        self.game.player_turn = 1
        x,y = self.game.play_alpha_beta()
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
    #     st = time.time()
    #     score = self.game.evaluation_function(state_board)
    #     print('\n\nThe calculate time is {}'.format(time.time()-st))
    #     print('The evaluation score is {}.\n\n'.format(score))
    #     return score
        # assert False

run = TTT_run()
run.teamId = '1304'  #1304
run.gameId = '3657'
run.op = op.operation("1304")
while True:
    if run.get_turn():
        run.get_state_board()
        x,y = run.make_decision()
        result=run.make_a_move(x,y)
        print("result",result)
        time.sleep(1)
    else:
        print("it is not team turn")
        time.sleep(1)
