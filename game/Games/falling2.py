import cv2

from game.framework import Game, CVMap
from game.physics2.bouncephysics import BouncePhysics
from game.physics2.WallPhysics import WallPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.Rectangle import Rectangle
from game.physics2.PixelPhysics import PixelPhysics
from game.test import test
from game.util.Vector2 import Vector2

G = 1
ppm = 50


class Falling2(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.r = Rectangle(200, 100, 50, 50)
        self.r1 = Rectangle(100, 100, 50, 50)
        self.c = Circle(100, 100, 50)
        self.physics = BouncePhysics()
        self.wall = WallPhysics()
        self.physics.objects.append(self.r)
        self.physics.objects.append(self.r1)
        self.physics.objects.append(self.c)

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map)
        self.wall.update_map(new_map)

    def update_game(self, keys, delta_t: int):
        for obj in self.physics.objects:
            obj.vy += ppm * G * delta_t

        # self.wall.update(delta_t)
        self.physics.update(delta_t)

        for obj in self.physics.objects:
            obj.translate(Vector2(obj.vx * delta_t, obj.vy * delta_t))

        self.r.draw(self.map.game_img)
        self.r1.draw(self.map.game_img)
        self.c.draw_hitbox(self.map.game_img)


test(Falling2, None)