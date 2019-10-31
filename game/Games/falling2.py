import cv2

from game.framework import Game, CVMap
from game.physics2.TempPhysics import TempPhysics
from game.physics2.WallPhysics import WallPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.Rectangle import Rectangle
from game.physics2.objects.rectanglephysics import RectanglePhysics
from game.test import test
from game.util.Vector2 import Vector2
from game.util.line import Line

G = .5
ppm = 50


class Falling2(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.c = Rectangle(100, 100, 50, 50)
        self.physics = RectanglePhysics()
        self.wall = WallPhysics()
        self.physics.objects.append(self.c)
        self.wall.objects.append(self.c)

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map)
        self.wall.update_map(new_map)

    def draw_circle(self, c: Circle):
        cv2.circle(self.map.game_img, (int(c.x), int(c.y)), int(c.r), 255)

    def update_game(self, keys, delta_t: int):
        c = self.c
        c.vy += ppm * G * delta_t

        # self.wall.update(delta_t)
        self.physics.update(delta_t)

        # c.x += c.vx * delta_t
        # c.y += c.vy * delta_t
        for i in c.pts:
            i += Vector2(c.vx * delta_t, c.vy * delta_t)

        c.draw(self.map.game_img)
        # self.draw_circle(self.c)


kms = Rectangle(50, 50, 100, 100)
#print(kms.inter(Line(Vector2(55, 0), Vector2(105, 50))))

test(Falling2)
