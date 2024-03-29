from typing import Tuple, List

import cv2
import numpy as np
import pygame

from game.Games.Ree.bullet import Living
from game.game import Game
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.objects.rectangle import Rectangle
from game.sound.sounds import load_sound
from game.util.vector2 import Vector2


class Enemy(Living):
    def __init__(self, m, hitbox: List[Tuple[float, float]], game):
        x, y, w, h = cv2.boundingRect(np.int32(hitbox))
        super().__init__(500, Vector2(x + w / 2, y + h / 2))

        self.is_rect = True
        self.hitbox: Tuple[float, float, float, float] = (x, x + w, y, y + h)
        self.max_health: float = 50
        self.health: float = 50
        self.cooldown = 1
        self.lastshot = 0
        self.game = game
        self.p_transform = m
        game.living.append(self)

        self.damage_sound = load_sound('ree/damaged.wav')

    def draw(self):
        surface = pygame.display.get_surface()
        pygame.draw.circle(surface, (255, 0, 0), self.game.map.cc(self.pos), 10)
        pygame.draw.rect(surface, (255, 0, 0), self.game.map.crr(self.hitbox), 10)
        self.draw_healthbar()

    def update(self, delta_t: float):
        if self.health > 0:
            self.lastshot += delta_t
            if self.health > 0 and self.lastshot >= self.cooldown:
                player_pos = self.game.player.pos
                dir = player_pos - self.pos
                self.game.add_bullet('1.png', Vector2(self.pos.x, self.pos.y),
                                     dir.unit() * self.game.map.pixels_per_meter,
                                     20, self)
                self.lastshot = 0

    def update_hitbox(self, m, new_hitbox: List[Tuple[int, int]]):
        x, y, w, h = cv2.boundingRect(np.int32(new_hitbox))
        self.pos = Vector2(x + w / 2, y + h / 2)
        self.hitbox = (x, x + w, y, y + h)
        self.p_transform = m

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return self.hitbox

    def draw_healthbar(self):
        bnds = self.get_bounds()
        ctr_x = (bnds[0] + bnds[1]) / 2
        bar_len, bar_w = 70, 6
        rect = self.game.map.cr((ctr_x - bar_len / 2, bnds[2] - 6 - bar_w, bar_len, bar_w))
        rect2 = self.game.map.cr(
            (ctr_x - bar_len / 2, bnds[2] - 6 - bar_w, bar_len * self.health / self.max_health, bar_w))
        pygame.draw.rect(self.game.map.surface, (255, 0, 0), rect)
        pygame.draw.rect(self.game.map.surface, (0, 255, 0), rect2)

    def damage(self, damage: float):
        super().damage(damage)
        self.damage_sound.play()
