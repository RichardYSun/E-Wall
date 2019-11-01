import cv2

from game.framework import Game, CVMap
from game.physics2.objects.PlatformCharacter import PlatformCharacter
from game.physics2.objects.PlatformCharacter2 import PlatformCharacter2
from game.test import test



class CharacterTest(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.c=PlatformCharacter(140,0,50,50)

    def update_game(self, keys, delta_t: int):
        self.c.update(self.map, delta_t)

        a=(int(self.c.x),int(self.c.y))
        b=(a[0]+self.c.w, a[1]+self.c.h)
        cv2.rectangle(self.map.game_img, a,b,255)


test(CharacterTest, )
