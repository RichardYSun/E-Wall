from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.physics import Physics
from game.util.vector2 import Vector2


class StandardPhysics(Physics):
    def __init__(self, gravity=Vector2(0, 9.81)):
        super().__init__()
        self.gravity = gravity

    def apply_physics(self, obj: PhysicsObject, delta_t):
        if self.gravity is not None:
            obj.vel += self.gravity * delta_t * self.map.pixels_per_meter
        obj.translate(obj.vel * delta_t)
