import cv2

class Bullet:
    px, py = 0.0
    angle = 0.0
    speed = 0.5
    image = None

    def __init__(self, px, py, speed, angle):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed

        image = cv2.imread('bulletBill.png', 1)

    def draw(self, img: cv2.ndarray):
        img[self.px: self.px + self.image.shape[0], self.py: self.py + self.image.shape[1]] = self.image