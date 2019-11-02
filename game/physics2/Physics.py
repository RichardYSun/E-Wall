from typing import List

from game.framework import CVMap
from game.physics2.objects.PhysicsObject import PhysicsObject


# applies physics between objects and map
class MapPhysics:
    def __init__(self):
        self.objects: List[PhysicsObject] = []
        self.map: CVMap = None

    def update_map(self, map: CVMap):
        self.map = map

    def update(self, delta_t: float):
        for obj in self.objects:
            self.apply_physics(obj, delta_t)

    def apply_physics(self, obj: PhysicsObject, delta_t):
        pass
