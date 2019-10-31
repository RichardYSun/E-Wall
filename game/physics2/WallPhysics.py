from game.physics2.Physics import MapPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.physics2.objects.Rectangle import Rectangle


class WallPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        if obj.obj_type == Circle.obj_type:
            obj: Circle
            if obj.y + obj.r >= self.map.edges.shape[0]:
                obj.y = self.map.edges.shape[0] - obj.r
                obj.vy = 0

            if obj.y - obj.r <= 0:
                obj.y = obj.r

            if obj.x - obj.r <= 0:
                obj.x = obj.r

            if obj.x + obj.r >= self.map.edges.shape[1]:
                obj.x = self.map.edges.shape[1] - obj.r
        elif obj.obj_type==Rectangle.obj_type:
            obj: Rectangle
