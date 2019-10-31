# represents a physical object
class PhysicsObject:
    obj_type: int
    x: float
    y: float
    vx = 0
    vy = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # called upon unsolvable physics situation
    def kill(self):
        pass
