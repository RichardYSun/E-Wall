import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.mag() < other.mag()

    def __gt__(self, other):
        return self.mag() > other.mag()

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def dot(a, b):
        return a.x * b.x + a.y * b.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, a):
        return Vector2(a * self.x, a * self.y)

    def __add__(self, a):
        return Vector2(self.x + a.x, self.y + a.y)

    def __sub__(self, a):
        return Vector2(self.x - a.x, self.y - a.y)
