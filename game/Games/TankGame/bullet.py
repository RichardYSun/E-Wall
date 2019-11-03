import cv2
import numpy as ndarray
import imutils

class Bullet:
    px = 0.0
    py = 0.0
    angle = 0.0
    speed = 0.5
    image = None
    damage = 9999.0
    radius = 10.0
    alive = True

    def __init__(self, px, py, speed, angle):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed

        image = cv2.imread('bulletBill.png', 1)

    def draw(self, img: ndarray):
        img[self.px: self.px + self.image.shape[0], self.py: self.py + self.image.shape[1]] = self.image

    def bounce(self, bouncedAngle):
        image = imutils.rotate_bound(self.image, bouncedAngle - self.angle)