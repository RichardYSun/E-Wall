import cv2

class Bullet:
    px, py = 0.0
    angle = 0.0
    speed = 0.5

    def __init__(self, px, py, speed, angle):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed

        image = cv2.imread('bulletBill.png', 1)

    def draw(self, img):
        img[x: x + image.shape[0], y: y + image.shape[1]] = image;