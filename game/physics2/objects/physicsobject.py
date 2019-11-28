# represents a physical object
from game.util.vector2 import Vector2


class PhysicsObject:
    obj_type: int

    def __init__(self, pos: Vector2):
        self.pos = pos
        self.vel = Vector2(0, 0)
        self.touching_top: bool = False
        self.touching_bottom: bool = False
        self.touching_left: bool = False
        self.touching_right: bool = False
        self.touching_wall:bool=False

    # called upon unsolvable physics situation
    def kill(self):
        pass

    def translate(self, move: Vector2):
        self.pos += move
