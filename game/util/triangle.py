import math
from typing import List

from game.util import vector2


class Triangle:
    def __init__(self, p1, p2, p3):
        self.pts = [p1, p2, p3]

    def area(self):
        pass
        # s = 0
        # l = []
        # for i in range(3):
        #     l.append((self.pts[i] - self.pts[(i + 1) % 3]).mag())
        #     s += l[i]
        #
        # s /= 2
        #
        # return math.sqrt(max(0, s * (s - l[0]) * (s - l[1]) * (s - l[2])))

