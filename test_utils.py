import time

import numpy as np
from unittest import TestCase
from utils import Game

class TestVairables_iter(TestCase):
    def setUp(self):
        self.game = Game(board_size=10, target=5)

    def test_evaluation_function(self):
        state_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='int8')
        st = time.time()
        score = self.game.evaluation_function(state_board)
        print('\n\nThe calculate time is {}'.format(time.time()-st))
        print('The evaluation score is {}.\n\n'.format(score))
        return score
        # assert False
