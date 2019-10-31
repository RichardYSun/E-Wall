from game.physics2.objects.PhysicsObject import PhysicsObject
from numpy import ndarray

class Circle(PhysicsObject):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def inter(self, lines: ndarray):
        pass
