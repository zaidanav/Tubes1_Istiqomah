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
        
    def pytagoras(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    
    def checkSekitar(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        range_xfirst = current_position.x - 14;
        range_yfirst = current_position.y - 14;
        range_xlast = current_position.x + 14;
        range_ylast = current_position.y + 14;
        jarak = 0;
        x = -1
        y = -1
        for i in range(range_xfirst, range_xlast+1):
            for j in range(range_yfirst, range_ylast+1):
                if i < 0 or i >= board.width or j < 0 or j >= board.height:
                    continue
                for game_object in board.game_objects:
                    if game_object.position.x == i and game_object.position.y == j and game_object.type == "DiamondGameObject": 
                        cek = False
                        red = False
                        for k in range(len(board.diamonds)):
                            if board.diamonds[k].position.x == i and board.diamonds[k].position.y == j and board.diamonds[k].properties.points == 2:
                                red = True
                            if board.diamonds[k].position.x == i and board.diamonds[k].position.y == j and board.diamonds[k].properties.points + props.diamonds > 5:
                                cek = True
                        if cek:
                            continue
                        if jarak == 0:
                            jarak = self.pytagoras(current_position.x, current_position.y, i, j)
                            x = i
                            y = j
                        else:
                            if jarak > self.pytagoras(current_position.x, current_position.y, i, j):
                                jarak = self.pytagoras(current_position.x, current_position.y, i, j)
                                x = i
                                y = j
        return (y, x)
    
    def isTaken(self, board: Board, x, y):
        for game_object in board.game_objects:
            if game_object.position.x == x and game_object.position.y == y and game_object.type != "DiamondGameObject":
                return True
        return False

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        current_position = board_bot.position
        sessionlegth = props.milliseconds_left
        if self.goal_position:
            isTaken = self.isTaken(board, self.goal_position.x, self.goal_position.y)
            if self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
                self.goal_position = None
            elif isTaken:
                self.goal_position = None
            
        if sessionlegth < 10000:
            if props.diamonds > 2:
                # Move to base
                base = board_bot.properties.base
                self.goal_position = base
            # elif props.diamonds == 0:
            #     check = self.checkSekitar(board_bot, board)
            #     if check[0] != -1:
            #         # Move to diamond
            #         self.goal_position = Position(check[0], check[1])
            #     else:
            #         # Just roam around
            #         self.goal_position = None
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
                self.current_direction = (self.current_direction + 1) % len(self.directions)
        return delta_x, delta_y