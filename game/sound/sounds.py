import os
import pygame

pygame.mixer.init()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_sound(sound: str):
    return pygame.mixer.Sound(ROOT_DIR + '/' + sound)
