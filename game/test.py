import os

import cv2
import time

import pygame as pygame

from game.imageio import ImageIO
from game.cv import CVer
import numpy as np

from game.keys import CV_MAPPING
from game.keys import PY_MAPPING
from game.util import ParamWindow


def test(G, cam='test2'):
    image_io = ImageIO(cam)

    map_detect = CVer()
    img = image_io.get_img()
    game = G(map_detect.do_cv(img))
    last_time = time.time()

    pygame.init()
    pygame.display.set_mode((100, 100))

    cnt = 0
    tt = 0

    keys_down = [False] * 5

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
        game.update_game(keys_down, t - last_time)
        tt += t - last_time
        last_time = t
        cnt += 1
        if tt > 1:
            print(cnt)
            tt = 0
            cnt = 0

        image_io.show(mp.game_img)

        # res = cv2.waitKey(1)
        # if res != -1:
        #     if res in CV_MAPPING:
        #         game.key_down(CV_MAPPING[res])
        #         game.key_up(CV_MAPPING[res])
        #     elif res == ord('q'):
        #         break

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in PY_MAPPING:
                    game.key_down(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = True
            if event.type == pygame.KEYUP:
                if event.key in PY_MAPPING:
                    game.key_up(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = False

    del image_io
