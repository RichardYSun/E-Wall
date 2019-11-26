from typing import List, Tuple

import pygame

from game.Games.Ree.stuart import Stuart
from game.game import Game, GameContext
from game.physics2.pixelphysics import PixelPhysics
from game.test import test
from game.util.vector2 import Vector2

class Ree(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.r = Stuart(Vector2(0, 0), mp)
        self.p = PixelPhysics()
        # self.w = WallPhysics()
        self.p.objects.append(self.r)
        # self.w.objects.append(self.r)

    def on_resize(self, size: Tuple[int, int]):
        self.r.on_resize(size)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.p.update_map(new_map)
        # self.w.update_map(new_map)
        self.r.update_map(new_map)

    def update_game(self, keys_down: List[bool], delta_t: int):
        self.p.update(delta_t)
        # self.w.update(delta_t)
        self.r.update(delta_t, keys_down)

        s = self.map.surface
        self.r.draw()
        pygame.display.flip()


if __name__ == "__main__":
    test(Ree, None)
