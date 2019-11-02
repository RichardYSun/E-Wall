from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.physics import Physics
from game.util.vector2 import Vector2


class Gravity(Physics):
    def __init__(self, g=Vector2(0, 9.81)):
        super().__init__()
        self.g = g

    def apply_physics(self, obj: PhysicsObject, delta_t):
        obj.vel += self.g * delta_t * self.map.pixels_per_meter
