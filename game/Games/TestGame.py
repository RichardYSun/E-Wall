from ..framework import Game
from ..test import test
import cv2


class TestGame(Game):

    def update_game(self, keys, delta_t: int):
        cv2.imshow('frame', self.map.edges)



