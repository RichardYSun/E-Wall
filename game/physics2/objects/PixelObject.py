from game.physics2.objects.PhysicsObject import PhysicsObject
from numpy import ndarray

from game.util.Vector2 import Vector2


class PixelObject(PhysicsObject):
    def draw_hitbox(self, img: ndarray):
        pass

    def get_bounds(self):
        pass

    def translate(self, move: Vector2):
        self.x += move.x
        self.y += move.y
