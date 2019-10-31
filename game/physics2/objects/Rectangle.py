import math
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util import line
from game.util.Vector2 import Vector2


class Rectangle(PhysicsObject):
    def __init__(self, x, y, l, h, a=0):
        super().__init__(x, y)
        self.pts.append(Vector2(x - l / 2 * math.cos(a), y - h / 2 * math.sin(a)))
        self.pts.append(Vector2(x - l / 2 * math.cos(a), y + h / 2 * math.sin(a)))
        self.pts.append(Vector2(x + l / 2 * math.cos(a), y - h / 2 * math.sin(a)))
        self.pts.append(Vector2(x + l / 2 * math.cos(a), y + h / 2 * math.sin(a)))

    def distance(self, l: line):
        ret = 0
        for i in self.pts:
            ret = min(ret, l.perp(i))
        return ret

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
