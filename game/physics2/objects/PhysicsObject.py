# represents a physical object
from game.util.Vector2 import Vector2


class PhysicsObject:
    obj_type: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = self.vy = 0

    # called upon unsolvable physics situation
    def kill(self):
        pass


    def translate(self, move: Vector2):
        self.x += move.x
        self.y += move.y