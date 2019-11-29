from typing import List, Tuple

from game.Games.Ree.generalenemy import GeneralEnemy


class Book(GeneralEnemy):
    def __init__(self, m, hitbox: List[Tuple[float, float]], game):
        super().__init__(m, hitbox, game, [(243,407),(400,300)], 400)
