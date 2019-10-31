from typing import Tuple

from game.physics2.objects.PhysicsObject import PhysicsObject

G = 9.8
PPM = 50


class PlatformCharacter(PhysicsObject):

    def __init__(self, x, y):
        super().__init__(x, y)

    # top,bottom,left,right
    def get_bounds(self) -> Tuple[int, int, int, int]:
        pass

