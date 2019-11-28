from typing import List, Tuple

import pygame
from cv2 import cv2
from numpy.core.multiarray import ndarray

from game.Games.Ree.bullet import Bullet, Living
from game.Games.Ree.player import Player
from game.cv.matcher import Matcher
from game.game import Game, GameContext
from game.physics2.pixelphysics import PixelPhysics, check_pixel_collision
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.vector2 import Vector2


class Ree(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.bullets: List[Bullet] = []
        self.living: List[Living] = []

        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()
        self.matcher = Matcher()
        self.frame = 0

        self.player = Player(Vector2(0, 0), self)
        self.pixel_physics.objects.append(self.player)
        self.living.append(self.player)
        self.wall_physics.objects.append(self.player)

    def on_resize(self, size: Tuple[int, int]):
        self.player.on_resize(size)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.player.update_map(new_map)
        self.frame += 1
        if self.frame == 48:
            self.frame = 0
            self.matcher.update_map(new_map)

    def add_bullet(self, img: str, pos: Vector2, vel: Vector2, damage: float, src, size=None):
        b = Bullet(self.map, pos, img, damage, vel, src, size)
        self.pixel_physics.objects.append(b)
        self.bullets.append(b)

    def remove_bullet(self, b: Bullet):
        self.pixel_physics.objects.remove(b)
        self.bullets.remove(b)

    def update_bullets(self, delta_t: float):
        for j in range(len(self.bullets) - 1, -1, -1):
            bul = self.bullets[j]
            bul.update(delta_t)
            flag = False

            for i in range(len(self.living) - 1, -1, -1):
                obj = self.living[i]
                if bul.src is not obj and check_pixel_collision(obj, bul) > 0:
                    obj.damage(bul.damage)
                    if obj.health <= 0:
                        obj.die()
                        del self.living[i]
                    self.remove_bullet(bul)
                    flag = True
                    break

            # if bullet is not already dead and collided with wall, remove it
            if not flag:
                if bul.death_flag:
                    del self.bullets[j]

    def update_game(self, keys_down: List[bool], delta_t: float):
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)

        self.player.update(delta_t, keys_down)

        self.update_bullets(delta_t)

        self.player.draw()
        for b in self.bullets:
            b.draw(self.map)

        pygame.display.flip()


if __name__ == "__main__":
    test(Ree, 'kust.bmp')  # '../ree/enemies/squaredude.jpg')
    # test(Ree,'smalldude3.jpg')
