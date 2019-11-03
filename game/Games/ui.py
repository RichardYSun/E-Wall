from datetime import time
from typing import List

import numpy as np
from cv2 import cv2, os

from game.Games.pong import Pong
from game.game import Game, GameContext

import game.keys as keys
from game.test import test

NUM_GAMES = 2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

games: List[Game] = [Pong]


class ui(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)
        self.selection = 0
        self.background = cv2.imread(ROOT_DIR + '/../img/selection.png')
        self.background = cv2.resize(self.background, None, fx=0.75, fy=0.75)
        self.arrow = cv2.imread(ROOT_DIR + '/../img/arrow.png')
        self.arrow = cv2.resize(self.arrow, None, fx=0.25, fy=0.25)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

    def draw_arrow(self, background, off):
        np.copyto(background[off[0]:self.arrow.shape[0] + off[0], off[1]:self.arrow.shape[1 ] + off[1]], self.arrow)

    def draw_ui(self):
        background = np.copy(self.background)

        self.draw_arrow(background, (180 + 100 * self.selection, 280))

        cv2.imshow('selection screen', background)

    def start_game(self):
        cv2.destroyWindow('selection screen')
        test(games[self.selection], None)

    def key_down(self, key: int):
        if key == keys.UP:
            self.selection = (self.selection + 1) % NUM_GAMES
        if key == keys.DOWN:
            self.selection = (self.selection - 1) % NUM_GAMES
        if key == keys.ENTER:
            self.start_game()

    def update_game(self, keys: List[bool], delta_t: int):
        self.draw_ui()


test(ui)
