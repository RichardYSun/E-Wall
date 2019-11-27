from typing import List, Tuple

import pygame
from cv2 import cv2
from numpy.core.multiarray import ndarray

from game.Games.Ree.player import Player
from game.cv.matcher import Matcher
from game.game import Game, GameContext
from game.img.images import imread
from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.pixelphysics import PixelPhysics
from game.test import test
from game.util.vector2 import Vector2
import numpy as np


class Enemy(PhysicsObject):
    def __init__(self, pos: Vector2, detect_img: ndarray):
        super().__init__(pos)


class Ree(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.player = Player(Vector2(0, 0), mp)
        self.pixel_physics = PixelPhysics()
        # self.w = WallPhysics()
        self.pixel_physics.objects.append(self.player)
        self.matcher = Matcher()
        # self.w.objects.append(self.r)
        self.frame = 0
        self.e = imread('test/book.jpg')
        h, w, d = self.e.shape
        self.r = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

        self.M = None

    def on_resize(self, size: Tuple[int, int]):
        self.player.on_resize(size)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.pixel_physics.update_map(new_map)
        # self.w.update_map(new_map)
        self.player.update_map(new_map)
        self.frame += 1
        if self.frame == 1:
            self.frame = 0
            self.matcher.update_img(new_map.original_img)
            k = self.matcher.match_obj(self.e)
            if len(k) > 0:
                self.M = k[0]
            else:
                self.M = None

    def update_game(self, keys_down: List[bool], delta_t: int):
        self.pixel_physics.update(delta_t)
        # self.w.update(delta_t)
        # self.player.update(delta_t, keys_down)

        s = self.map.surface
        # self.player.draw()

        if self.M is not None:
            nr = cv2.perspectiveTransform(self.r, self.M)
            r = []
            print('ye')
            for a in nr:
                x, y = a[0][0], a[0][1]
                r.append(self.map.cc((x * self.map.downscale, y * self.map.downscale)))
            pygame.draw.polygon(self.map.surface, (255, 0, 0), r, 2)

        pygame.display.flip()


if __name__ == "__main__":
    test(Ree, None)#'../ree/enemies/squaredude.jpg')
    #test(Ree,'smalldude3.jpg')
