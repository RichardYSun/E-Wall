import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.mag() < other.mag()

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def dot(a, b):
        return a.x * b.x + a.y * b.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def mult(self, a):
        return Vector2(a * self.x, a * self.y)

    def add(a, b):
        return Vector2(a.x + b.x, a.y + b.y)
