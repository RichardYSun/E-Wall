import math

from game.physics2.Physics import MapPhysics
from game.physics2.PixelPhysics import PixelPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.physics2.slidephysics import SlidePhysics
from game.util.Vector2 import Vector2

bounce = 1


class BouncePhysics(MapPhysics):
    def __init__(self):
        super().__init__()
        self.pixel_physics = PixelPhysics()
        self.slide_physics = SlidePhysics()

    def apply_physics(self, obj: PhysicsObject, delta_t):
        edges = self.map.edges

        normal = self.pixel_physics.teleport(obj, edges)

        if normal.sq_mag() != 0:
            self.slide_physics.slide(obj, edges, normal)

        # cnt = 0
        #
        # angleSum = 0
        #
        # for p in self.map.lines:
        #     p = (p[0][0], p[0][1])
        #
        #     d = obj.distance(p)
        #     a = obj.angle(p)
        #     if d is not None:
        #         xx, yy = d
        #         obj.x += xx
        #         obj.y += yy
        #         cnt += 1
        #         angleSum += a
        #
        # if cnt == 0:
        #     return
        #
        # # angle = weightedAngleSum / weightedNum
        # angle = angleSum / cnt
        #
        # velocity = Vector2(obj.vx, obj.vy)
        # vAngle = math.atan2(-obj.vy, -obj.vx)
        #
        # newAngle = angle + angle - vAngle
        #
        # # print(str(angle * 180 / math.pi) + " " + str(vAngle * 180 / math.pi) + " " + str(newAngle * 180 / math.pi))
        #
        # obj.vx = velocity.mag() * math.cos(newAngle) * bounce
        # obj.vy = velocity.mag() * math.sin(newAngle) * bounce
