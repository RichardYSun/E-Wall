from typing import List

from game.game import GameContext
from game.physics2.objects.physicsobject import PhysicsObject


class Physics:
    def __init__(self):
        self.objects: List[PhysicsObject] = []
        self.map: GameContext = None

    def update_map(self, map: GameContext):
        self.map = map

    def update(self, delta_t: float):
        for obj in self.objects:
            self.apply_physics(obj, delta_t)

    def apply_physics(self, obj: PhysicsObject, delta_t):
        pass
