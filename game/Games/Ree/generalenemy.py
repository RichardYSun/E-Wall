from typing import Tuple, List

import cv2
import numpy as np
import pygame

from game.Games.Ree.bullet import Living
from game.sound.sounds import load_sound
from game.util.vector2 import Vector2


class GeneralEnemy(Living):
    def __init__(self, m, hitbox: List[Tuple[float, float]], game,
                 shoot_pts: List[Tuple[float, float]], health: float,
                 bul_img: str = '1.png',
                 damage_sound: str = 'ree/damaged.wav', shoot_sound: str = 'ree/pew.wav',
                 cooldown=1.0, ):
        x, y, w, h = cv2.boundingRect(np.int32(hitbox), )
        super().__init__(health, Vector2(x + w / 2, y + h / 2))

        self.is_rect = True

        self.game = game
        self.p_transform = m

        self.s = 10
        s = self.s
        self.hitbox: Tuple[float, float, float, float] = (x - s, x + s + w, y - s, y + s + h)

        self.o_pts = shoot_pts
        self.shoot_pts = self.cvt_pts(self.o_pts)

        self.cooldown = cooldown
        self.lastshot = 0
        self.bul_img = bul_img

        self.damage_sound = load_sound(damage_sound)
        self.shoot_sound = load_sound(shoot_sound)

        game.living.append(self)

    def cvt_pts(self, pts):
        k = np.float32(pts).reshape(-1, 1, 2)
        return cv2.perspectiveTransform(k, self.p_transform)

    def draw(self):
        surface = pygame.display.get_surface()
        pygame.draw.circle(surface, (255, 0, 0), self.game.map.cc(self.pos), 10)
        pygame.draw.rect(surface, (255, 0, 0), self.game.map.crr(self.hitbox), 10)
        self.draw_healthbar()

    def update(self, delta_t: float):
        if self.health > 0:
            self.lastshot += delta_t
            if self.lastshot >= self.cooldown:
                player_pos = self.game.player.pos
                self.shoot_sound.play()
                for pt in self.shoot_pts:
                    pos = Vector2(pt[0][0], pt[0][1]) * self.game.map.downscale
                    dire = player_pos - pos
                    self.game.add_bullet(self.bul_img, pos,
                                         dire.unit() * self.game.map.pixels_per_meter,
                                         20, self)
                self.lastshot = 0

    def update_hitbox(self, m, new_hitbox: List[Tuple[int, int]]):
        self.shoot_pts = self.cvt_pts(self.o_pts)
        x, y, w, h = cv2.boundingRect(np.int32(new_hitbox))
        self.pos = Vector2(x + w / 2, y + h / 2)
        s = self.s
        self.hitbox = (x - s, x + s + w, y - s, y + s + h)
        self.p_transform = m

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return self.hitbox

    def draw_healthbar(self):
        bounds = self.get_bounds()
        ctr_x = (bounds[0] + bounds[1]) / 2
        bar_len, bar_w = 70, 6
        rect = self.game.map.cr((ctr_x - bar_len / 2, bounds[2] - 6 - bar_w, bar_len, bar_w))
        rect2 = self.game.map.cr(
            (ctr_x - bar_len / 2, bounds[2] - 6 - bar_w, bar_len * self.health / self.max_health, bar_w))
        pygame.draw.rect(self.game.map.surface, (255, 255, 255), rect)
        pygame.draw.rect(self.game.map.surface, (255, 255, 255), rect2)

    def damage(self, damage: float):
        super().damage(damage)
        self.damage_sound.play()
