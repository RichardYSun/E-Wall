import os

import cv2
import time

from game.ImageIO import ImageIO
from game.cv import CVer
import numpy as np


def test(G, cam=False):
    if cam:
        image_io = ImageIO(None)
    else:
        image_io = ImageIO()

    map_detect = CVer()
    img = image_io.get_img()
    game = G(img)
    last_time = time.time()

    while True:
        img = image_io.get_img()

        mp = map_detect.do_cv(img)
        game_img = mp.edges
        mp.game_img = mp.lsd.drawSegments(game_img, mp.lines)

        game.update_map(mp)

        t = time.time()
        game.update_game([], t - last_time)
        last_time = t

        image_io.show(mp.game_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del image_io
