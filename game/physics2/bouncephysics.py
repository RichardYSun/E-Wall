from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject

class BouncePhysics(MapPhysics):
    def apply_physics(self, obj: PhysicsObject, delta_t):

        cnt = 0

        weightedAngleSum = 0
        weightedNum = 0

        angleSum = 0

        for p in self.map.lines:
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
