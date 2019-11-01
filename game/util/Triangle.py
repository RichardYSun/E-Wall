import math
from typing import List

from game.util import Vector2


class Triangle:
    def __init__(self, p1, p2, p3):
        self.pts = [p1, p2, p3]

    def area(self):
        s = 0
        l = []
        for i in range(3):
            l.append((self.pts[i] - self.pts[(i + 1) % 3]).mag())
            s += l[i]

        s /= 2

        return math.sqrt(max(0, s * (s - l[0]) * (s - l[1]) * (s - l[2])))

        # x1, y1 = self.pts[0].x, self.pts[0].y
        # x2, y2 = self.pts[1].x, self.pts[1].y
        # x3, y3 = self.pts[2].x, self.pts[2].y
        # return 1 / 2 * abs((x1 * y2 + x2 * y3 + x3 * y1) - (x1 * y3 + x2 * y1 + x3 * y2))