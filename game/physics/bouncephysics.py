import cv2
import math
from game.physics.Vector2 import Vector2

from game.physics.physics import Physics, PhysicsObject


def force(x):
    return x * x


class AnglePhysics(Physics):
    def kustify(self, obj: PhysicsObject):
        img = obj.img(self.edges)
        inter = cv2.bitwise_and(self.edges, img)
        non = cv2.findNonZero(inter)
        if non is None:
            return
        cnt = 0

        weightedAngleSum = 0
        weightedNum = 0

        angleSum = 0

        for p in non:
            p = (p[0][0], p[0][1])
            d = obj.distance(p)
            a = obj.angle(p)
            if d is not None:
                xx, yy = d
                obj.x += xx
                obj.y += yy
                cnt += 1

                mag = math.sqrt(xx * xx + yy * yy)
                weightedAngleSum += a * mag
                weightedNum += mag

                angleSum += a

        if cnt == 0:
            return

        # angle = weightedAngleSum / weightedNum
        angle = angleSum / cnt

        velocity = Vector2(obj.vx, obj.vy)
        vAngle = math.atan2(-obj.vy, -obj.vx)

        newAngle = angle + angle - vAngle

        # print(str(angle * 180 / math.pi) + " " + str(vAngle * 180 / math.pi) + " " + str(newAngle * 180 / math.pi))

        obj.vx = 0.2 * velocity.mag() * math.cos(newAngle)
        obj.vy = 0.2 * velocity.mag() * math.sin(newAngle)
