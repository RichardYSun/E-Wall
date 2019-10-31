from game.physics2.Physics import MapPhysics
from game.physics2.objects import PhysicsObject


class RectanglePhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        lines = self.edges.lines
        for i in lines:
            perp = obj.distance(i)

