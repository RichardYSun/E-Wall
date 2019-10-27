import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
