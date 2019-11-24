import os

import pygame
from pygame.font import Font

pygame.font.init()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_font(name: str, size: int)->Font:
    return pygame.font.Font(ROOT_DIR+'/'+name, size)
