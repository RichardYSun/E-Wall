from typing import Tuple

import cv2
import pygame
from numpy.core._multiarray_umath import ndarray

from game.game import GameContext
from game.img.images import load_py_img, imread
from game.util.vector2 import Vector2


class AnimationState:
    def __init__(self, img: str, game_size: Tuple[float, float] = None,
                 timer: float = None,
                 next_state: str = None, scale: float = None):
        self.o_py_img: pygame.Surface = load_py_img(img).convert_alpha()

        self.cv_img: ndarray = cv2.extractChannel(imread(img, cv2.IMREAD_UNCHANGED), 3)
        self.py_img: pygame.Surface = None

        self.next_state: str = next_state
        self.timer: float = timer
        if game_size is None:
            game_size = self.o_py_img.get_size()
        if scale is not None:
            game_size = (int(game_size[0]*scale), int(game_size[1]*scale))
        self.game_size = game_size
        self.cv_img = cv2.resize(self.cv_img, game_size)

    def load(self, mp: GameContext):
        self.py_img = mp.conv_img(self.o_py_img, self.game_size)
