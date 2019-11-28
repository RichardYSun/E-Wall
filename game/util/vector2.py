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
        return self.sq_mag() < other.sq_mag()

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def sq_mag(self):
        return self.x * self.x + self.y * self.y

    ##projects the other vector onto the current one
    def proj(self, other):
        return self * (self.dot(other) // self.sq_mag())

    def cross(self, other):
        return abs(self.x * other.y - self.y * other.x)

    def angle(self, other):
        a=self.dot(other) / self.mag() / other.mag()
        return math.acos(max(-1,min(1,a)))

    def unit(self):
        return self / self.mag()

    def as_tuple(self):
        return self.x, self.y

    def as_int_tuple(self):
        return int(self.x), int(self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, other):
        return Vector2(other * self.x, other * self.y)

    def __add__(self, a):
        return Vector2(self.x + a.x, self.y + a.y)

    def __sub__(self, a):
        return Vector2(self.x - a.x, self.y - a.y)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __str__(self):
        return str(int(self.x)) + " " + str(int(self.y))

    def perp_vector(self):
        return Vector2(self.y, -self.x)
