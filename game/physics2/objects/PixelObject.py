from game.physics2.objects.PhysicsObject import PhysicsObject
from numpy import ndarray

from game.util.Vector2 import Vector2


class PixelObject(PhysicsObject):
    def draw_hitbox(self, img: ndarray):
        pass

    def get_bounds(self):
        pass

    def on_collision(self, offset:Vector2):
        self.vx=self.vy=0
        self.translate(offset)
