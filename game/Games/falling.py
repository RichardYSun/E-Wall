import cv2
import time

from game.framework import Game, CVMap
from game.test import test


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0


G = 9.8


class Falling(Game):

    def __init__(self, mp: CVMap):
        self.c = Circle(10, 10, 10)
        self.lastTime = time.time()
        Game.__init__(self, mp)

    def draw_circle(self, c: Circle):
        cv2.circle(self.map.edges, (int(c.x), int(c.y)), int(c.r), 255)

    def update_game(self, keys, delta_t: int):
        # if self.map is None:
        #     return
        self.c.vy += G * (time.time() - self.lastTime)
        self.c.y += self.c.vy * (time.time() - self.lastTime)
        self.lastTime = time.time()
        self.draw_circle(self.c)
        cv2.imshow('frame', self.map.edges)


test(Falling)
