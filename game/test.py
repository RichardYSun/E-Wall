import os

import cv2
import time

from game.ImageIO import ImageIO
from game.cv import CVer
import numpy as np


def test(G, still=None):
    image_io = ImageIO()

    map_detect = CVer()
    game = G(image_io.get_img())
    last_time = time.time()

    game_img=np.zeros((1000,500,3),dtype=np.uint8)

    while True:
        img = image_io.get_img()
        mp = map_detect.do_cv(img)
        game.update_map(mp)
        t = time.time()
        img = game.update_game([], t - last_time, game_img)
        last_time = t
        image_io.show(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del image_io
