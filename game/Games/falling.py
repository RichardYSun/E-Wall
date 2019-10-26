import cv2

from game.framework import Game, CVMap
from game.physics import Circle, Physics, ShittyPhysics
from game.test import test

G = 9.8
ppm=1


class Falling(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.c = Circle(30, 30, 10)
        self.physics = ShittyPhysics()

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map.edges)

    def draw_circle(self, c: Circle):
        cv2.circle(self.map.edges, (int(c.x ), int(c.y )), int(c.r), 255)

    def update_game(self, keys, delta_t: int):
        # if self.map is None:
        #     return
        self.c.vy += ppm*G * delta_t

        self.c.x += self.c.vx * delta_t
        self.c.y += self.c.vy * delta_t

        self.physics.kustify(self.c)

        self.draw_circle(self.c)
        return self.map.edges


test(Falling)
