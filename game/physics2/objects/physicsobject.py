# represents a physical object
from game.util.vector2 import Vector2


class PhysicsObject:
    obj_type: int

    def __init__(self, pos: Vector2):
        self.pos = pos
        self.vel = Vector2(0, 0)
        self.touching_top: bool = None
        self.touching_bottom: bool = None
        self.touching_left: bool = None
        self.touching_right: bool = None

    # called upon unsolvable physics situation
    def kill(self):
        pass

    def translate(self, move: Vector2):
        self.pos += move
