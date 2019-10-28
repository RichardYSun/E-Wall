import cv2
import math
from game.util.Vector2 import Vector2

from game.physics.physics import Physics, PhysicsObject


def force(x):
    return x * x


class BouncePhysics(Physics):

    #takes an object and applies physics to it
    #object will bounce off of surface
    #bounce is the velocity conserved after the object bounces
    #for example, if bounce is 0.8, the final speed will be 80% of the initial speedmd
    def kustify(self, obj: PhysicsObject, bounce):
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


        obj.vx = velocity.mag() * math.cos(newAngle) * bounce
        obj.vy = velocity.mag() * math.sin(newAngle) * bounce
