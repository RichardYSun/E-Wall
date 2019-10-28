from typing import List

from game.framework import CVMap
from game.physics2.objects import PhysicsObject


# applies physics between objects and map
class MapPhysics:
    map: CVMap
    objects: List[PhysicsObject]

    def update_map(self, map: CVMap):
        self.map = map

    def update(self, delta_t: float):
        for obj in self.objects:
            self.apply_physics(obj, delta_t)

    def apply_physics(self, obj: PhysicsObject, delta_t):
        pass
