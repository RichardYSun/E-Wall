from typing import Tuple

import cv2
import numpy as np

from game.framework import CVMap
from game.physics2.objects.PhysicsObject import PhysicsObject

G = 9.8
PPM = 50


class PlatformCharacter(PhysicsObject):
    obj_type = 3

    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.grounded = False
        self.fx = self.fy = 0

        self.thres_ground = 1

    def update(self, map: CVMap, delta_t: float):


        sub_rect = map.edges[self.x:self.x + self.w, self.y:self.y + self.w]
        locs = np.nonzero(sub_rect)
        t, l, b, r = -1, -1, 99999, 99999
        ct, cb, cl, cr = 0, 0, 0, 0
        for p in locs:
            x, y = p
            if x < self.x:
                cl += 1
                l = max(l, x)
            else:
                cr += 1
                r = min(r, x)

            if y < self.y:
                ct += 1
                t = max(t, y)
            else:
                cb += 1
                b = min(b, y)

        self.grounded = cb >= self.thres_ground

        #collision


        if not self.grounded:
            self.vy += PPM * G * delta_t

        self.x = self.x + self.vx * delta_t
        self.y = self.y + self.vy * delta_t
