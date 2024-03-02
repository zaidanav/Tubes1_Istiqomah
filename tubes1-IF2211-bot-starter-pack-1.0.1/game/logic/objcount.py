import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def count (self, board_bot: GameObject, board: Board, center):
    count = 0
    range_xfirst = center.x - 6
    range_yfirst = center.y - 6
    range_xlast = center.x + 6
    range_ylast = center.y + 6
    jarak = 0
    x = -1
    y = -1
    for i in range(range_xfirst, range_xlast+1):
        for j in range(range_yfirst, range_ylast+1):
            if i < 0 or i >= board.width or j < 0 or j >= board.height:
                continue
            for game_object in board.game_objects:
                if game_object.position.x == i and game_object.position.y == j and (game_object.type == "DiamondGameObject"):
                    count += 1
    return count

