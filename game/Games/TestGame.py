from ..framework import Game
import cv2


class TestGame(Game):

    def update_game(self, keys, delta_t: int):
        cv2.imshow('frame', self.map.edges)
