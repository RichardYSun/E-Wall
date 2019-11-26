import time

import pygame as pygame

# from game.buttonData import button
from game.imageio import ImageIO
from game.cv import CVer

from game.keys import PY_MAPPING, ARDUINO_MAPPING
from game.util import ParamWindow
from game.img.images import conv_cv_to_py


def test(G, cam='ree'):
    image_io = ImageIO(cam)

    map_detect = CVer()
    stupid = image_io.get_img()
    map_detect.do_cv(stupid)
    game = G(stupid)
    last_time = time.time()
    game.on_resize(stupid.pysize)

    cnt = 0
    tt = 0

    keys_down = [False] * 10

    while True:
        new_sz = None
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                new_sz = event.dict['size']
                pygame.display.set_mode(new_sz, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key in PY_MAPPING:
                    game.key_down(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = True
            if event.type == pygame.KEYUP:
                if event.key in PY_MAPPING:
                    game.key_up(PY_MAPPING[event.key])
                    keys_down[PY_MAPPING[event.key]] = False

        # curKey = button()
        # buttonID = curKey.buttonID
        # state = curKey.state
        #
        # for index in ARDUINO_MAPPING:
        #     if index == buttonID:
        #         if state == 1:
        #             game.key_down(ARDUINO_MAPPING[buttonID])
        #         if state == 0:
        #             game.key_up(ARDUINO_MAPPING[buttonID])



        ctx = image_io.get_img()

        map_detect.do_cv(ctx)

        show_edges = ParamWindow.get_int('show edges', 1, 1)
        if show_edges:
            pixels = pygame.transform.scale(conv_cv_to_py(ctx.edges), ctx.surface.get_size())
            ctx.surface.blit(pixels, (0, 0))
        else:
            ctx.surface.fill((255, 255, 255))

        game.update_map(ctx)

        if new_sz is not None:
            game.on_resize(new_sz)


        t = time.time()
        game.update_game(keys_down, min(t - last_time,0.1))
        tt += t - last_time
        last_time = t
        cnt += 1
        if tt > 1:
            print(cnt)
            tt = 0
            cnt = 0

    del image_io
