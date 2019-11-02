from typing import Tuple

import cv2
import numpy as np

from game.framework import CVMap
from game.physics2.objects.PhysicsObject import PhysicsObject

G = 9.8
PPM = 50


class PlatformCharacter2(PhysicsObject):
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
        locs = cv2.findNonZero(sub)

        nx = 0
        ny = 0
        nxc = 0
        nyc = 0

        if locs is not None:
            for p in locs:
                x, y = p[0]
                if x - 1 >= 0 and sub[y, x - 1] == 0:
                    nx += x - w
                    nxc += 1
                if x + 1 < w and sub[y, x + 1] == 0:
                    nx += x
                    nxc += 1
                if y - 1 >= 0 and sub[y - 1, x] == 0:
                    ny += y - h
                    nyc += 1
                if y + 1 < w and sub[y + 1, x] == 0:
                    ny += y
                    nyc += 1

        if nxc != 0:
            self.x = nx / nxc + sx
            self.vx = self.vy = 0

        if nyc != 0:
            ny = ny / nyc + sy
            self.grounded = ny < sy
            self.vx = self.vy = 0
        else:
            self.grounded = False

        if not self.grounded:
            self.vy += PPM * G * delta_t

        self.x = self.x + self.vx * delta_t
        self.y = self.y + self.vy * delta_t

        self.x %= map.game_img.shape[1]
        self.y %= map.game_img.shape[0]
