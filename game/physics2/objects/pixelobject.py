from game.physics2.collisiontypes import COLLISION_NONE
from game.physics2.objects.physicsobject import PhysicsObject
from numpy import ndarray

from game.util.vector2 import Vector2

class PixelObject(PhysicsObject):
    collision_escape_radius = 10
    collision_type = COLLISION_NONE

    def __init__(self, pos):
        super().__init__(pos)
        self.collision_escape_vector: Vector2 = None

    # should draw the hitbox of this image onto img
    # img is a uint8 array with the size of the game image
    def draw_hitbox(self, img: ndarray):
        pass

    # should return the rectangular bounding box for this object
    # in the form left,right,top,bottom
    def get_bounds(self):
        pass
