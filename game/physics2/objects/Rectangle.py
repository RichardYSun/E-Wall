import math

import cv2

from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util import line
from game.util.Triangle import Triangle
from game.util.Vector2 import Vector2
from game.util.line import Line


class Rectangle(PhysicsObject):
    va = [0, 0, 0, 0]

    obj_type = 2

    def __init__(self, x, y, l, h, a=0):
        super().__init__(x, y)
        self.pts = []
        self.pts.append(Vector2(x - l / 2, y - h / 2))
        self.pts.append(Vector2(x - l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y - h / 2))
        self.area = l * h
        self.l = l
        self.h = h

    # rotates angle by theta radians about pt
    def rotate(self, theta, pt):
        for i in range(4):
            if i != pt:
                dif = self.pts[i] - self.pts[pt]
                angle = math.atan2(dif.y, dif.x)
                angle += theta
                new_dif = Vector2(dif.mag() * math.cos(angle), dif.mag() * math.sin(angle))
                self.pts[i] = pt + new_dif

    def distance(self, l: line):
        ret = Vector2(1e5, 1e5)
        for i in self.pts:
            d = l.distance(i)
            if self.inside(i - d):
                ret = min(ret, d)
        return ret

    def closest(self, l: line):
        mn = Vector2(1e5, 1e5)
        ret = -1
        for i in range(4):
            if self.inside(self.pts[i] - l.distance(self.pts[i])) and l.distance(self.pts[i]) < mn:
                mn = l.distance(self.pts[i])
                ret = i
        return ret

    def inside(self, pt: Vector2):
        a = 0
        for i in range(4):
            x1, y1 = self.pts[i].x, self.pts[i].y
            x2, y2 = self.pts[(i + 1) % 4].x, self.pts[(i + 1) % 4].y
            x3, y3 = pt.x, pt.y
            a += 0.5 * abs((x1 * y2 + x2 * y3 + x3 * y1) - (x1 * y3 + x2 * y1 + x3 * y2))

        return abs(a - self.area) < 1e-3

    def inter(self, line: Line):
        for i in self.pts:
            if self.inside(i - line.distance(i)):
                return 1
        return 0

    def draw(self, img):
        for i in range(4):
            cv2.line(img, (int(self.pts[i].x), int(self.pts[i].y)),
                     (int(self.pts[(i + 1) % 4].x), int(self.pts[(i + 1) % 4].y)), 255, 2)

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
