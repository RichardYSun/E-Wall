from game.util.Vector2 import Vector2


class Line:

    def __init__(self, st: Vector2, ed: Vector2):
        self.st: Vector2 = st
        self.ed: Vector2 = ed

        # # variables for equation of line ax + by + c = 0
        # self.a = ed.y - st.y
        # self.b = st.x - ed.x
        # self.c = -(self.a * st.x + self.b * st.y)

        self.dir: Vector2 = self.ed - self.st

    def perp(self, pt: Vector2):
        diag = Vector2(pt.x - self.st.x, pt.y - self.st.y)
        return diag - self.dir * diag.dot(self.dir) * (1 / self.dir.mag() / self.dir.mag())

    def distance(self, pt: Vector2):
        ret = min((self.st - pt).mag(), (self.ed - pt).mag())

        perp: Vector2 = self.perp(pt)
        inter: Vector2 = pt - perp
        if max((self.st - inter).mag(), (self.ed - inter).mag()) <= self.dir.mag():
            ret = min(ret, perp.mag())

        return ret
