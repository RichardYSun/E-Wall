import time

import pygame as pygame

from game.game import GameContext
from game.imageio import ImageIO
from game.cv import CVer

from game.keys import PY_MAPPING


def test(G, cam='test2', use_pygame=True):
    image_io = ImageIO(cam)

    map_detect = CVer()
    stupid = image_io.get_img()
    map_detect.do_cv(stupid)
    game = G(stupid)
    last_time = time.time()

    cnt = 0
    tt = 0

    keys_down = [False] * 10

    while True:
        ctx = image_io.get_img()

        map_detect.do_cv(ctx)

        game.update_map(ctx)

        t = time.time()
        game.update_game(keys_down, t - last_time)
        tt += t - last_time
        last_time = t
        cnt += 1
        if tt > 1:
            print(cnt)
            tt = 0
            cnt = 0

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key in PY_MAPPING:
                    game.key_down(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = True
            if event.type == pygame.KEYUP:
                if event.key in PY_MAPPING:
                    game.key_up(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = False

    del image_io
