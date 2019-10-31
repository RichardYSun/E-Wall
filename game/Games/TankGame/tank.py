import cv2
import imutils


class Tank:
    px, py = 0.0
    angle = 0.0  # radians
    speed = 0.0
    sprite: cv2.ndarray

    def __init__(self, px, py, speed, angle, type: int):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed
        if type == 1:
            self.sprite = cv2.imread('player.jpg')
        elif type == 2:
            self.sprite = cv2.imread('blue.jpg')
        elif type == 3:
            self.sprite = cv2.imread('red.jpg')

    def rotateRight(self, TurnSpeed):
        self.sprite = imutils.rotate_bound(self.image, -TurnSpeed)

    def rotateLeft(self, TurnSpeed):
        self.sprite = imutils.rotate_bound(self.image, TurnSpeed)

    def draw(self, game_img: cv2.ndarray):
        game_img[self.px: self.px + self.sprite.shape[0], self.py: self.py + self.sprite.shape[1]] = self.sprite
