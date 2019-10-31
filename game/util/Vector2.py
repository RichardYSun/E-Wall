import math


# class representing a 2D vector
# Construct a vector with components x, y: Vector2(x, y)
# operators supported:
# add/subtract two vectors: va +/- vb
# dot two vectors: va.dot(vb)
# compare magnitude of two vectors: va < vb (I don't have > yet)
# magnitude of a vector: va.mag()
# multiply/divide a vector by a scalar: va * or / t

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.mag() < other.mag()

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        return Vector2(other * self.x, other * self.y)

    def __add__(self, a):
        return Vector2(self.x + a.x, self.y + a.y)

    def __sub__(self, a):
        return Vector2(self.x - a.x, self.y - a.y)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)
