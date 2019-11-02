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
        self.edge = 0
        self.ww = 0
        self.hh = 0

    def update(self, map: CVMap, delta_t: float):
        x, y = int(self.x), int(self.y)
        sub_rect = map.edges[y:y + self.h, x:x + self.w]
        locs = cv2.findNonZero(sub_rect)
        t, l, b, r = -1, -1, 99999, 99999
        ct, cb, cl, cr = 0, 0, 0, 0

        cx, cy = self.w / 2.0, self.h / 2.0
        if locs is not None:
            for p in locs:
                x, y = p[0]

                if x < cx and sub_rect[y, x + 1] == 0:
                    cl += 1
                    l = max(l, x)
                if x > cx and sub_rect[y, x - 1] == 0:
                    cr += 1
                    r = min(r, x)

                if y < cy and sub_rect[y + 1,x] == 0:
                    ct += 1
                    t = max(t, y)
                if y > cy and sub_rect[y - 1,x] == 0:
                    cb += 1
                    b = min(b, y)

        self.grounded = cb > 0


        self.vy += PPM * G * delta_t

        t += self.y
        b += self.y - self.h
        l += self.x
        r += self.x - self.w

        # collision
        if cb > self.hh and ct > self.hh:
            self.vy = 0
            self.y = (t + b) / 2
        else:
            if cb > self.hh:
                self.y = b+1
                self.vy = abs(self.vy) * self.bounce
            elif ct > self.hh:
                self.y = t-1
                self.vy = abs(self.vy) * -self.bounce

        if cl > self.ww and cr > self.ww:
            self.vx = 0
            self.x = (l + r) / 2
        else:
            if cl > self.ww:
                self.x = l-1
                self.vx = abs(self.vx) * self.bounce
            elif cr > self.ww:
                self.x = r+1
                self.vx = abs(self.vx) * -self.bounce

        self.x = self.x + self.vx * delta_t
        self.y = self.y + self.vy * delta_t

        self.x %= map.game_img.shape[1]
        self.y %= map.game_img.shape[0]
