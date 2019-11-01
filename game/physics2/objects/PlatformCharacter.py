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

        self.bounce = 0

    def update(self, map: CVMap, delta_t: float):
        x, y = int(self.x), int(self.y)
        sub_rect = map.edges[y:y + self.h, x:x + self.w]
        locs = cv2.findNonZero(sub_rect)
        t, l, b, r = -1, -1, 99999, 99999
        ct, cb, cl, cr = 0, 0, 0, 0
        if locs is not None:
            for p in locs:
                x, y = p[0]
                if x < self.w / 2:
                    cl += 1
                    l = max(l, x)
                else:
                    cr += 1
                    r = min(r, x)

                if y < self.h / 2:
                    ct += 1
                    t = max(t, y)
                else:
                    cb += 1
                    b = min(b, y)

        self.grounded = cb > 0

        if self.grounded:
            self.vy = 0
        else:
            self.vy += PPM * G * delta_t

        t += self.y
        b += self.y-self.h
        l += self.x
        r += self.x-self.w

        # collision
        if cb > 0 and ct > 0:
            self.vy = 0
            self.y = (t + b) / 2
        else:
            if cb > 0:
                self.y = b
                self.vy = abs(self.vy) * self.bounce
            elif ct > 0:
                self.y = t
                self.vy = abs(self.vy) * -self.bounce

        if cl > 0 and cr > 0:
            self.vx = 0
            self.x = (l + r) / 2
        else:
            if cl > 0:
                self.x = l
                self.vx = abs(self.vx) * self.bounce
            elif cr > 0:
                self.x = r
                self.vx = abs(self.vx) * -self.bounce

        self.x = self.x + self.vx * delta_t
        self.y = self.y + self.vy * delta_t

        self.x %= map.game_img.shape[1]
        self.y %= map.game_img.shape[0]
