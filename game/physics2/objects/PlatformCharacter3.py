from typing import Tuple

import cv2
import numpy as np

from game.framework import CVMap
from game.physics2.objects.PhysicsObject import PhysicsObject

G = 9.8
PPM = 50


class PlatformCharacter3(PhysicsObject):
    obj_type = 3

    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.grounded = False
        self.fx = self.fy = 0

        self.bounce = 0
        self.edge = 0
        self.ww = w
        self.hh = h

    def update(self, map: CVMap, delta_t: float):
        sx, sy = int(self.x), int(self.y)
        w, h = self.w, self.h
        sub = map.edges[sy:sy + h, sx:sx + w]

        ax, ay = 0.0, 0.0
        cnt = 0
        for x in range(w):
            for y in range(h):
                print(x,y)
                if sub[y, x] == 0:
                    cnt += 1
                    ax += x
                    ay += y

        ny = ay / cnt + self.y - h / 2
        self.x = ax / cnt + self.x - w / 2
        self.vy += PPM * G * delta_t
        if ny < self.y:
            self.vy = 0

        self.y = ny

        self.x = self.x + self.vx * delta_t
        self.y = self.y + self.vy * delta_t

        self.x %= map.game_img.shape[1]
        self.y %= map.game_img.shape[0]
