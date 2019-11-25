from typing import Tuple

from game.physics2.collisiontypes import COLLISION_NONE
from game.physics2.objects.physicsobject import PhysicsObject
from numpy import ndarray

from game.util.vector2 import Vector2


class PixelObject(PhysicsObject):

    def __init__(self, pos):
        super().__init__(pos)
        self.collision_escape_vector: Vector2 = None

        self.collision_escape_radius: int = 10
        self.collision_type: int = COLLISION_NONE
        self.is_rect: bool = False
        self.use_direct_img: bool = False

    # should draw the hitbox of this image onto img
    # img is a uint8 array with the size of the game image
    def draw_hitbox(self, img: ndarray):
        pass

    # should directly return the hitbox image
    # this is more efficient
    # it is assumed the top left corner is at pos
    def get_hitbox(self) -> ndarray:
        pass

    # should return the rectangular bounding box for this object
    # in the form left,right,top,bottom
    def get_bounds(self) -> Tuple[int, int, int, int]:
        if self.use_direct_img:
            xmn = int(self.pos.x)
            ymn = int(self.pos.y)
            hitbox = self.get_hitbox()
            xmx = xmn + hitbox.shape[1]
            ymx = ymn + hitbox.shape[0]
            return xmn, xmx, ymn, ymx
