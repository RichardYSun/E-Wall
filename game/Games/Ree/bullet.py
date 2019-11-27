from game.physics2.objects.pixelobject import PixelObject


class Bullet(PixelObject):
    def __init__(self, pos):
        super().__init__(pos)
