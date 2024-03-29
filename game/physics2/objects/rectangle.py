import math

import cv2

from game.physics2.objects.circle import Circle
from game.physics2.objects.pixelobject import PixelObject
from game.util import line
from game.util.vector2 import Vector2
from game.util.line import Line
import numpy as np
from numpy import ndarray


class Rectangle(PixelObject):

    def __init__(self, pos, l, h):
        super().__init__(pos)
        x, y = pos.x, pos.y
        self.pts = []
        self.pts.append(Vector2(x - l / 2, y - h / 2))
        self.pts.append(Vector2(x - l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y - h / 2))
        self.area = l * h
        self.l = l
        self.h = h

    # rotates angle by theta radians about pt
    def rotate(self, theta: float, pt: Vector2):
        for i in range(4):
            dif = self.pts[i] - pt
            angle = math.atan2(dif.y, dif.x)
            angle += theta
            new_dif = Vector2(dif.mag() * math.cos(angle), dif.mag() * math.sin(angle))
            self.pts[i] = pt + new_dif

    # warning: does not work if you don't rotate about centre
    def circle_collision(self, other: Circle):
        dir = self.pos - other.pos
        return self.inside(other.pos + dir * (other.r / dir.mag()))

    def inside(self, pt: Vector2):
        a = 0
        for i in range(4):
            x1, y1 = self.pts[i].x, self.pts[i].y
            x2, y2 = self.pts[(i + 1) % 4].x, self.pts[(i + 1) % 4].y
            x3, y3 = pt.x, pt.y
            a += 0.5 * abs((x1 * y2 + x2 * y3 + x3 * y1) - (x1 * y3 + x2 * y1 + x3 * y2))
        return abs(a - self.area) < 1e-3

    def draw(self, img):
        for i in range(4):
            cv2.line(img, (int(self.pts[i].x), int(self.pts[i].y)),
                     (int(self.pts[(i + 1) % 4].x), int(self.pts[(i + 1) % 4].y)), 255, 2)

    def get_bounds(self):
        xmn = ymn = 1e9
        xmx = ymx = 0

        for i in range(4):
            xmn = min(xmn, int(self.pts[i].x))
            xmx = max(xmx, int(self.pts[i].x))
            ymn = min(ymn, int(self.pts[i].y))
            ymx = max(ymx, int(self.pts[i].y))

        xmx += 1
        ymx += 1

        return xmn, xmx, ymn, ymx

    def draw_hitbox(self, img: ndarray):
        pts = np.array((
            (self.pts[0].x, self.pts[0].y),
            (self.pts[1].x, self.pts[1].y),
            (self.pts[2].x, self.pts[2].y),
            (self.pts[3].x, self.pts[3].y)
        ), dtype=int)
        cv2.fillConvexPoly(img, pts, 255)

    def translate(self, move: Vector2):
        self.pos += move
        for i in range(4):
            self.pts[i] += move

# def points(self):
#     x = [-self.l / 2, self.l / 2]
#     y = [-self.h / 2, self.h / 2]
#     pts = []
#
#     for i in range(2):
#         for j in range(2):
#             angle = self.a + math.atan2(y[j], x[i])
#             mag = math.sqrt(y[j] * y[j] + x[i] * x[i])
#             pts.append((int(self.x + mag * math.cos(angle)), int(self.y + mag * math.sin(angle))))
#
#     tmp = pts[2]
#     pts[2] = pts[3];
#     pts[2] = tmp
#
#     return pts
