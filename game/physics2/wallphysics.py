from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.physics import Physics
from game.physics2.objects.circle import Circle
from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.objects.rectangle import Rectangle
from game.util.vector2 import Vector2


class WallPhysics(Physics):
    def __init__(self, ):
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        super().__init__()

    def apply_physics(self, obj: PhysicsObject, delta_t):
        if isinstance(obj, PixelObject):
            xmn, xmx, ymn, ymx = obj.get_bounds()
            obj.touching_top = self.top and ymn < 0
            if obj.touching_top:
                obj.translate(Vector2(0, -ymn + 1))
                if obj.collision_type == COLLISION_BOUNCE:
                    obj.vel.y *= -1
                else:
                    obj.vel.y = 0
            obj.touching_bottom = self.bottom and ymx >= self.map.height
            if obj.touching_bottom:
                obj.translate(Vector2(0, self.map.height - ymx))
                if obj.collision_type == COLLISION_BOUNCE:
                    obj.vel.y *= -1
                else:
                    obj.vel.y = 0
            obj.touching_bottom = self.left and xmn < 0
            if obj.touching_bottom:
                obj.translate(Vector2(-xmn + 1, 0))
                if obj.collision_type == COLLISION_BOUNCE:
                    obj.vel.x *= -1
                else:
                    obj.vel.x = 0
            obj.touching_right = self.right and xmx >= self.map.width
            if obj.touching_right:
                obj.translate(Vector2(self.map.width - xmx - 1, 0))
                if obj.collision_type == COLLISION_BOUNCE:
                    obj.vel.x *= -1
                else:
                    obj.vel.x = 0
