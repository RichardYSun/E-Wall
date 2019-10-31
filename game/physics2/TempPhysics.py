from game.physics2.Physics import MapPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2
from game.util.line import Line


class TempPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):

        if obj is Circle:
            for line in self.map.lines:
                x1, y1, x2, y2, _ = line
                l = Line(Vector2(x1, y1), Vector2(x2, y2))

