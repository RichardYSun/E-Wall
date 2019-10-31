from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject


class TempPhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):
        for line in self.map.lines:
            x1,y1,x2,y2,_=line
