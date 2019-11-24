from typing import List, Tuple

import pygame
from cv2 import os

from game.Games.pong import Pong
from game.Games.TankGame.tankGame2 import TankGame2
from game.game import Game, GameContext

import game.keys as keys
from game.test import test
from game.img import images

NUM_GAMES = 2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

games: List[Game] = [Pong, TankGame2]


class ui(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)
        self.selection = 0
        self.background: pygame.Surface = None
        self.arrow: pygame.Surface = None
        self.start = 0

    def on_resize(self, size: Tuple[int, int]):
        mp = self.map
        self.background = mp.conv_img(images.load_py_img('selection.png'), mp.size)
        self.arrow = mp.conv_img(images.load_py_img('arrow.png'), mp.size / 8)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

    def draw_arrow(self, surface, off):
        surface.blit(self.arrow, off)

    def draw_ui(self):
        mp = self.map
        self.map.image_py(self.background, (0, 0), )
        self.map.image_py(self.arrow, (mp.width / 4, mp.height / 3 + mp.height / 5 * self.selection), )

        pygame.display.update()

    def start_game(self):
        test(games[self.selection], None)

    def key_down(self, key: int):
        if key == keys.UP1:
            self.selection = (self.selection + 1) % NUM_GAMES
        if key == keys.DOWN1:
            self.selection = (self.selection - 1) % NUM_GAMES
        if key == keys.FIRE1 and not self.start:
            self.start = 1
            self.start_game()

    def update_game(self, keys: List[bool], delta_t: int):
        self.draw_ui()


if __name__ == "__main__":
    test(ui)
