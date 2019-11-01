# represents a physical object
class PhysicsObject:
    obj_type: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = self.vy = 0

    # called upon unsolvable physics situation
    def kill(self):
        pass
