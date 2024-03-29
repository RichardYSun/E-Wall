import os

from typing import Dict, Tuple

import cv2
import numpy
import pygame
from numpy.core.multiarray import ndarray

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

py_img_cache: Dict[str, pygame.Surface] = {}
cv_img_cache: Dict[Tuple[str, int], ndarray] = {}


def py_resize(img: pygame.Surface, size: Tuple[int, int])-> pygame.Surface:
    return pygame.transform.scale(img, size)


def load_py_img(file) -> pygame.Surface:
    if file not in py_img_cache:
        py_img_cache[file] = pygame.image.load(ROOT_DIR + '/' + file)
        # if scale is not None:
        #     size = py_img_cache[key].get_size()
        #     size = (int(size[0] * scale), int(size[1] * scale))
        #
        # if size != 'none':
        #     size = map(int, size)
        #     py_img_cache[key] = pygame.transform.scale(py_img_cache[key], size)
    return py_img_cache[file]


def imread(file, mode=cv2.IMREAD_COLOR) -> ndarray:
    key = (file, mode)
    if key not in py_img_cache:
        cv_img_cache[key] = cv2.imread(ROOT_DIR + '/' + file, mode)
        # if size != 'none':
        #     size = map(int, size)
        #     cv_img_cache[key] = cv2.resize(cv_img_cache[key], size)
    return cv_img_cache[key]


def conv_cv_to_py(img: ndarray):
    return pygame.transform.flip(pygame.surfarray.make_surface(numpy.rot90(img)), 1, 0)
