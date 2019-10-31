import cv2

from game.framework import Game, CVMap
from game.physics2.TempPhysics import TempPhysics
from game.physics2.objects.Circle import Circle
from game.test import test

G = 9.8
ppm = 50


class Falling(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.c = Circle(200, 10, 50)
        self.physics = TempPhysics()
        self.physics.objects.append(self.c)

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map)

    def draw_circle(self, c: Circle):
        cv2.circle(self.map.game_img, (int(c.x), int(c.y)), int(c.r), 255)

    def update_game(self, keys, delta_t: int):
        # if self.map is None:
        #     return
        c = self.c
        c.vy += ppm * G * delta_t

        self.physics.update(delta_t)
        c.x += c.vx * delta_t
        c.y += c.vy * delta_t

        if c.y + c.r >= self.map.edges.shape[0]:
            c.y = self.map.edges.shape[0] - c.r
            c.vy = 0

        self.draw_circle(self.c)


test(Falling)
