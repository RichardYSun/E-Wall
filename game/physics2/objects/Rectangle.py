import math

import cv2

from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util import line
from game.util.Triangle import Triangle
from game.util.Vector2 import Vector2
from game.util.line import Line


class Rectangle(PhysicsObject):
    obj_type = 2

    def __init__(self, x, y, l, h, a=0):
        super().__init__(x, y)
        self.pts = []
        self.pts.append(Vector2(x - l / 2, y - h / 2))
        self.pts.append(Vector2(x - l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y + h / 2))
        self.pts.append(Vector2(x + l / 2, y - h / 2))
        self.area = l * h

    def distance(self, l: line):
        ret = Vector2(1e5, 1e5)
        for i in self.pts:
            if self.inside(i - l.distance(i)):
                ret = min(ret, l.distance(i))
        return ret

    def inside(self, pt: Vector2):
        a = 0
        for i in range(4):
            a += Triangle(pt, self.pts[i], self.pts[(i + 1) % 4]).area()

        return abs(a - self.area) < 1e-6

    def inter(self, line: Line):
        ret = 0;
        for i in self.pts:
            print(i.__str__ ()+ " " + (i - line.distance(i)).__str__())
            ret |= self.inside(i - line.distance(i))
        return ret

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
