from game.util.Vector2 import Vector2


class Line:

    def __init__(self, st: Vector2, ed: Vector2):
        self.st = st
        self.ed = ed

        # # variables for equation of line ax + by + c = 0
        # self.a = ed.y - st.y
        # self.b = st.x - ed.x
        # self.c = -(self.a * st.x + self.b * st.y)

        self.dir = self.ed - self.st

    def perp(self, pt: Vector2):
        diag = Vector2(pt.x - self.st.x, pt.y - self.st.y)
        return Vector2.add(diag, dir.mult(-1 * Vector2.dot(diag, dir) / dir.mag() / dir.mag()))
