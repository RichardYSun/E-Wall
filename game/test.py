import os

import cv2
import time

from game.imageio import ImageIO
from game.cv import CVer
import numpy as np

from game.util import ParamWindow


def test(G, cam='test2'):
    image_io = ImageIO(cam)

    map_detect = CVer()
    img = image_io.get_img()
    game = G(map_detect.do_cv(img))
    last_time = time.time()

    cnt = 0
    tt = 0
    while True:
        img = image_io.get_img()

        mp = map_detect.do_cv(img)

        show_edges = ParamWindow.get_int('show edges', 1, 1)
        if show_edges == 1:
            mp.game_img = mp.edges
        else:
            mp.game_img = np.zeros_like(mp.edges)
        mp.game_img = mp.lsd.drawSegments(mp.game_img, mp.lines)

        game.update_map(mp)

        t = time.time()
        game.update_game([], t - last_time)
        tt += t - last_time
        last_time = t
        cnt += 1
        if tt > 1:
            print(cnt)
            tt = 0
            cnt = 0

        image_io.show(mp.game_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del image_io
