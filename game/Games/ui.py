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
        self.arrow = cv2.imread(ROOT_DIR + '/../img/arrow.png')
        print(self.arrow.shape)
        self.arrow = cv2.resize(self.arrow, None, fx=0.25, fy=0.25)
        print(self.arrow.shape)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

    def draw_arrow(self, background, off):
        np.copyto(background[off[0]:self.arrow.shape[0] + off[0], off[1]:self.arrow.shape[1] + off[1]], self.arrow)

    def draw_ui(self):
        background = np.copy(self.background)

        self.draw_arrow(background, (120 + 100 * self.selection, 220))

        cv2.imshow('selection screen', background)

    def start_game(self):
        test(games[self.selection])

    def update_game(self, keys: List[bool], delta_t: int):
        if keys.UP:
            self.selection = (self.selection + 1) % NUM_GAMES
        if keys.DOWN:
            self.selection = (self.selection - 1) % NUM_GAMES
        if 1:
            self.start_game()

        self.draw_ui()


test(ui)
