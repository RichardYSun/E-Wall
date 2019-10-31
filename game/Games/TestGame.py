from game.framework import Game, CVMap
from game.test import test
import cv2


class TestGame(Game):

    def update_game(self, keys, delta_t: int):
        return self.map.edges


test(TestGame, None)
