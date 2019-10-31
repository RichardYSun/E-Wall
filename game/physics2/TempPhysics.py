from game.physics2.Physics import MapPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2
from game.util.line import Line


class TempPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):

        if obj.obj_type == Circle.obj_type:
            obj: Circle
            for l in self.map.lines_conv:
                perp = l.distance(Vector2(obj.x, obj.y))
                mag = perp.mag()
                dcenter = obj.r - mag
                if dcenter > 0:
                    opp = perp * (-dcenter / mag)
                    obj.x += opp.x
                    obj.y += opp.y
                    obj.vx = obj.vy = 0

        else:
            print("warning: applying tempphysics to non-circle")
