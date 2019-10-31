from game.physics2.Physics import MapPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.PhysicsObject import PhysicsObject


class WallPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        if obj.obj_type == Circle.obj_type:
            obj: Circle
            if obj.y + obj.r >= self.map.edges.shape[0]:
                obj.y = self.map.edges.shape[0] - obj.r
                obj.vy = -obj.vy

            if obj.y - obj.r <= 0:
                obj.y = obj.r
                obj.vy = -obj.vy

            if obj.x - obj.r <= 0:
                obj.x = obj.r
                obj.vx = -obj.vx

            if obj.x + obj.r >= self.map.edges.shape[1]:
                obj.x = self.map.edges.shape[1] - obj.r
                obj.vx = -obj.vx
        else:
            pass
            #print("warning: WallPhysics not implemented for rectangle")
