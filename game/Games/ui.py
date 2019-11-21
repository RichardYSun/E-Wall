from datetime import time
from typing import List

import numpy as np
import pygame
from cv2 import cv2, os

# from game.Games.pong import Pong
# from game.Games.TankGame.tankGame import TankGame
from game.game import Game, GameContext

import game.keys as keys
from game.test import test
from game.util import moreimutils

NUM_GAMES = 2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# games: List[Game] = [Pong,TankGame]


class ui(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)
        self.selection = 0
        # self.background = cv2.imread(ROOT_DIR + '/../img/selection.png')
        # self.background = cv2.resize(self.background, None, fx=0.75, fy=0.75)
        # self.arrow = cv2.imread(ROOT_DIR + '/../img/arrow.png')
        # self.arrow = cv2.resize(self.arrow, None, fx=0.25, fy=0.25)
        self.surface = pygame.display.get_surface()
        self.background = moreimutils.get_py_img('selection.png', None,
                                                 self.surface.get_size())
        self.arrow = moreimutils.get_py_img('arrow.png', None,
                                            (self.surface.get_width() // 8, self.surface.get_height() // 8))
        self.start = 0

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

    def draw_arrow(self, off):
        # np.copyto(background[off[0]:self.arrow.shape[0] + off[0], off[1]:self.arrow.shape[1] + off[1]], self.arrow)
        self.surface.blit(self.arrow, off)

    def draw_ui(self):
        # background = np.copy(self.background)
        self.background = pygame.transform.scale(self.background, self.surface.get_size())
        self.arrow = pygame.transform.scale(self.arrow, (self.surface.get_width() // 8, self.surface.get_height() // 8))

        self.surface.blit(self.background, (0, 0))

        self.draw_arrow((self.surface.get_width() // 4,
                         self.surface.get_height() // 3 + self.surface.get_height() // 5 * self.selection))

        pygame.display.update()
        # cv2.imshow('selection screen', background)

    def start_game(self):
        cv2.destroyWindow('selection screen')
        # test(games[self.selection], None)

    def key_down(self, key: int):
        if key == keys.UP:
            self.selection = (self.selection + 1) % NUM_GAMES
        if key == keys.DOWN:
            self.selection = (self.selection - 1) % NUM_GAMES
        if key == keys.ENTER and not self.start:
            self.start = 1
            self.start_game()

    def update_game(self, keys: List[bool], delta_t: int):
        self.draw_ui()


test(ui)
