from game.physics2.Physics import MapPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.physics2.objects.PixelObject import PixelObject
from game.physics2.objects.Rectangle import Rectangle
from game.util.Vector2 import Vector2


class WallPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        if isinstance(obj, PixelObject):
            xmn, xmx, ymn, ymx = obj.get_bounds()
            if xmn<0:
                obj.translate(Vector2(-xmn, 0))
                obj.vx*=-1
            if xmx>=self.map.width:
                obj.translate(Vector2(self.map.width-xmx, 0))
                obj.vx*=-1

