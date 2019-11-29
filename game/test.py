import os
import time

import cv2
import pygame as pygame

from game.buttonData import button
from game.game import GameContext
from game.imageio import ImageIO
from game.cv.edgedetector import EdgeDetector

from game.keys import PY_MAPPING, ARDUINO_MAPPING
from game.util import ParamWindow
from game.img.images import conv_cv_to_py

import threading


def derp(image_io, edge_detector, game, g_lock: threading.Lock):
    prev_size = (0, 0)
    while True:
        # get new webcam image
        ctx: GameContext = image_io.get_img()

        # image processing
        edge_detector.detect_edges(ctx)

        # give game new edges
        game.update_map(ctx)

        h, w = ctx.original_img.shape[:2]

        if w != prev_size[0] or h != prev_size[1]:
            game.on_resize(ctx.pysize)

        cv2.waitKey(1)

        prev_size = (w, h)


def test(G, cam='ree'):
    pygame.init()
    image_io = ImageIO(cam)
    edge_detector = EdgeDetector()

    # get initial frame
    first_frame = image_io.get_img()
    edge_detector.detect_edges(first_frame)

    # initialize game
    game = G(first_frame)
    game.on_resize(first_frame.pysize)

    frame_count = 0
    total_time = 0

    keys_down = [False] * 12

    g_lock = threading.RLock()
    x = threading.Thread(target=derp, args=(image_io, edge_detector, game, g_lock))
    x.start()

    last_time = time.time()
    while x.is_alive():
        # process pygame events
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

        # process arduino events
        cur_key = button()
        if cur_key is not None:
            button_id = cur_key.buttonID
            state = cur_key.state

            for index in ARDUINO_MAPPING:
                if index == button_id:
                    if state == 1:
                        game.key_down(ARDUINO_MAPPING[button_id])
                    if state == 0:
                        game.key_up(ARDUINO_MAPPING[button_id])

        # debug
        show_edges = ParamWindow.get_int('show edges', 1, 1)

        # with g_lock:
        ctx: GameContext = game.map
        # g_lock.acquire()
        if show_edges:
            pixels = pygame.transform.scale(conv_cv_to_py(ctx.edges), ctx.surface.get_size())
            ctx.surface.blit(pixels, (0, 0))
        else:
            ctx.surface.fill((0, 0, 0))
        cv2.imshow('edges', ctx.edges)
        # tell game if window has resized
        if new_sz is not None:
            game.on_resize(new_sz)

        # update game
        cur_time = time.time()
        game.update_game(keys_down, min(cur_time - last_time, 0.1))
        # g_lock.release()
        total_time += cur_time - last_time

        # print fps
        last_time = cur_time
        frame_count += 1
        if total_time > 1:
            print(frame_count)
            total_time = 0
            frame_count = 0
        cv2.waitKey(1)

    del image_io
