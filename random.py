import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    def checkSekitar(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        range_xfirst = current_position.x - 2;
        range_yfirst = current_position.y - 2;
        range_xlast = current_position.x + 2;
        range_ylast = current_position.y + 2;
        for i in range(range_xfirst, range_xlast+1):
            for j in range(range_yfirst, range_ylast+1):
                if i < 0 or i >= board.width or j < 0 or j >= board.height:
                    continue
                for game_object in board.game_objects:
                    if game_object.position.x == i and game_object.position.y == j and game_object.type == "DiamondGameObject":
                        return j ,i
        return -1, -1

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        current_position = board_bot.position
        print("Current: ", current_position)
        
        if self.goal_position and self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
            self.goal_position = None
        if self.goal_position == None:    
            check = self.checkSekitar(board_bot, board)
            if props.diamonds == 5:
                # Move to base
                base = board_bot.properties.base
                self.goal_position = base
            elif check[0] != -1:
                # Move to diamond
                self.goal_position = Position(check[0], check[1])
            else:
                # Just roam around
                self.goal_position = None
        print("Goal: ", self.goal_position)
        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y