import pygame

UP1 = 1
DOWN1 = 2
LEFT1 = 3
RIGHT1 = 0
ACTIONA1 = 4
ACTIONB1 = 5


UP2 = 6
DOWN2 = 7
LEFT2 = 8
RIGHT2 = 11
ACTIONA2 = 9
ACTIONB2 = 10


CV_MAPPING = {
    ord('w'): UP1,
    ord('a'): LEFT1,
    ord('s'): DOWN1,
    ord('d'): RIGHT1,
    13: ACTIONA1

}

PY_MAPPING = {
    pygame.K_w: UP1,
    pygame.K_a: LEFT1,
    pygame.K_s: DOWN1,
    pygame.K_d: RIGHT1,
    pygame.K_SPACE: ACTIONA1,

    pygame.K_UP: UP2,
    pygame.K_LEFT: LEFT2,
    pygame.K_DOWN: DOWN2,
    pygame.K_RIGHT: RIGHT2,
    pygame.K_RETURN: ACTIONA2
}

ARDUINO_MAPPING = {
    2: UP1,
    3: RIGHT1,
    4: DOWN1,
    5: LEFT1,
    6: ACTIONA1,
    7: ACTIONB1,

    8: UP2,
    9: RIGHT2,
    10: DOWN2,
    11: LEFT2,
    12: ACTIONA2,
    13: ACTIONB2,

}