import numpy as np

from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2


class SlidePhysics:
    def __init__(self):
        pass

    def slide(self, obj: PhysicsObject, edges: np.ndarray, normal: Vector2):
        dir = Vector2(normal.y, -normal.x)
        vel = Vector2(obj.vx, obj.vy)
        new_vel = dir.proj(vel)
        obj.vx, obj.vy = new_vel.x, new_vel.y

        # print(obj.vx, obj.vy)
        print(vel.__str__() + " " + dir.__str__())
