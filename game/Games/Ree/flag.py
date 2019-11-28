from typing import Tuple, List

import cv2
import numpy as np
import pygame

from game.game import Game
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.objects.rectangle import Rectangle
from game.physics2.pixelphysics import PixelPhysics, check_pixel_collision
from game.util.vector2 import Vector2


class Flag(PixelObject):
    def __init__(self, m, hitbox: List[Tuple[float, float]], game):
        x, y, w, h = cv2.boundingRect(np.int32(hitbox))
        super().__init__(Vector2(x + w / 2, y + h / 2))

        self.is_rect = 1
        self.hitbox: Tuple[float, float, float, float] = (x, x + w, y, y + h)
        self.game = game
        self.p_transform = m

    def draw(self):
        surface = pygame.display.get_surface()
        pygame.draw.circle(surface, (0, 255, 0), self.game.map.cc(self.pos), 10)

    def update_hitbox(self, m, new_hitbox: List[Tuple[int, int]]):
        x, y, w, h = cv2.boundingRect(np.int32[new_hitbox])
        self.pos = Vector2(x + w / 2, y + h / 2)
        self.hitbox = (x, x + w, y, y + h)
        self.p_transform = m

    def rect_intersect(self, r1: List[Tuple[float, float]], r2: List[Tuple[float, float]]):
        rect = [max(r1[0], r2[0]), min(r1[1], r2[1]), max(r1[2], r2[2]), min(r1[3], r2[3])]
        return rect[0] < rect[1] and rect[2] < rect[3]

    def update(self):
        if check_pixel_collision(self, self.game.player) > 0:
            self.game.win()

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return self.hitbox
