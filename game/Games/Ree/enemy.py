from typing import Tuple, List

import cv2
import numpy as np
import pygame

from game.game import Game
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.objects.rectangle import Rectangle
from game.util.vector2 import Vector2


class Enemy(PixelObject):
    def __init__(self, m, hitbox: List[Tuple[float, float]], game):
        x, y, w, h = cv2.boundingRect(np.int32(hitbox))
        super().__init__(Vector2(x + w / 2, y + h / 2))

        self.is_rect = 1
        self.hitbox: Tuple[float, float, float, float] = (x, x + w, y, y + h)
        self.health: float = 50
        self.cooldown = 1
        self.lastshot = 0
        self.game = game
        self.p_transform = m

    def draw(self):
        surface = pygame.display.get_surface()
        pygame.draw.circle(surface, (255, 0, 0), self.game.map.cc(self.pos), 10)

    def update(self, delta_t: float):
        self.lastshot += delta_t
        if self.health > 0 and self.lastshot >= self.cooldown:
            print('shoot')
            player_pos = self.game.player.pos
            dir = player_pos - self.pos
            self.game.add_bullet('1.png', Vector2(self.pos.x, self.pos.y), dir.unit() * self.game.map.pixels_per_meter,
                                 20, self)
            self.lastshot = 0

    def update_hitbox(self, m, new_hitbox: List[Tuple[int, int]]):
        x, y, w, h = cv2.boundingRect(np.int32[new_hitbox])
        self.pos = Vector2(x + w / 2, y + h / 2)
        self.hitbox = (x, x + w, y, y + h)
        self.p_transform = m

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return self.hitbox
