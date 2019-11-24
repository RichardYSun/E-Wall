from game.physics2.collisiontypes import COLLISION_NONE
from game.physics2.objects.physicsobject import PhysicsObject
from numpy import ndarray

from game.util.vector2 import Vector2


class PixelObject(PhysicsObject):

    def __init__(self, pos):
        super().__init__(pos)
        self.collision_escape_vector: Vector2 = None

        self.collision_escape_radius:int = 10
        self.collision_type:int = COLLISION_NONE
        self.is_rect:bool = False

    # should draw the hitbox of this image onto img
    # img is a uint8 array with the size of the game image
    def draw_hitbox(self, img: ndarray):
        pass

    def get_img(self)->ndarray:
        pass

    # should return the rectangular bounding box for this object
    # in the form left,right,top,bottom
    def get_bounds(self):
        pass
