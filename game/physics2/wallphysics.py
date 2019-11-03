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
            if self.top and ymn < 0:
                obj.translate(Vector2(0, -ymn + 1))
                obj.vel.y *= -1
            if self.bottom and ymn >= self.map.height:
                obj.translate(Vector2(0, self.map.height - ymx - 1))
                obj.vel.y *= -1
            if self.left and xmn < 0:
                obj.translate(Vector2(-xmn + 1, 0))
                obj.vel.x *= -1
            if self.right and xmn >= self.map.width:
                obj.translate(Vector2(self.map.width - xmx - 1, 0))
                obj.vel.x *= -1
