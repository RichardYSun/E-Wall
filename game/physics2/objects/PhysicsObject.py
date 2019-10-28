# represents a physical object
class PhysicsObject:
    x = 0
    y = 0
    vx = 0
    vy = 0

    # called upon unsolvable physics situation
    def kill(self):
        pass
