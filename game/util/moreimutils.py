import os

from typing import Dict, Tuple

import cv2
import numpy
import pygame
from numpy.core.multiarray import ndarray

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

py_img_cache: Dict[Tuple[str, Tuple[int, int]], pygame.Surface] = {}
cv_img_cache: Dict[Tuple[str, str, Tuple[int, int]], ndarray] = {}


def get_py_img(file, scale=None, size=None, ) -> pygame.Surface:
    if size is None:
        size = 'none'
    key = (file, size)
    if key not in py_img_cache:
        py_img_cache[key] = pygame.image.load(ROOT_DIR + '/../img/' + file)
        if scale is not None:
            size = py_img_cache[key].get_size()
            size = (int(size[0] * scale), int(size[1] * scale))

        if size != 'none':
            py_img_cache[key] = pygame.transform.scale(py_img_cache[key], size)
    return py_img_cache[key]


def imread(file, mode=cv2.IMREAD_COLOR, size=None) -> ndarray:
    if size is None:
        size = 'none'
    key = (file, mode, size)
    if key not in py_img_cache:
        print(ROOT_DIR + '/../img/' + file)
        cv_img_cache[key] = cv2.imread(ROOT_DIR + '/../img/' + file, mode)
        if size != 'none':
            cv_img_cache[key] = cv2.resize(cv_img_cache[key], size)
    return cv_img_cache[key]


def conv_cv_to_py(img: ndarray):
    return pygame.transform.flip(pygame.surfarray.make_surface(numpy.rot90(img)), 1, 0)
