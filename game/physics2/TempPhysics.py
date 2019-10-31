from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject


class TempPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        