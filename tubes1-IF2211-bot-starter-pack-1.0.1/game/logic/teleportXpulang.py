import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class TelePulang(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.teleport: Optional[Position] = None
        self.isTeleport = False
        self.current_direction = 0
        self.idTeleport = -1
        
    def pytagoras(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    def countSteps(self, goal: Position, current: Position):
        return abs(goal.x - current.x) + abs(goal.y - current.y)

    def count(self,board: Board, center):
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
                   
    def NewCheckSekitar(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        jarak = 0
        x = -1
        y = -1        
        for objek in board.game_objects:
            if objek.type == "DiamondGameObject" or objek.type == "TeleportGameObject": 
                if objek.type == "TeleportGameObject":
                    for tele in board.game_objects:
                        if tele.type == "TeleportGameObject" and tele.id != objek.id: 
                            if self.count(board, tele.position) < 5:
                                continue
                cek = False
                if objek.type == "DiamondGameObject":
                    for k in range(len(board.diamonds)):
                        if board.diamonds[k].position.x == objek.position.x and board.diamonds[k].position.y == objek.position.y and board.diamonds[k].properties.points + props.diamonds > 5:
                            cek = True
                if cek:
                    continue
                if jarak == 0:
                    jarak = self.pytagoras(current_position.x, current_position.y, objek.position.x, objek.position.y)
                    x = objek.position.x
                    y = objek.position.y
                else:
                    if jarak > self.pytagoras(current_position.x, current_position.y, objek.position.x, objek.position.y):
                        jarak = self.pytagoras(current_position.x, current_position.y, objek.position.x, objek.position.y)
                        x = objek.position.x
                        y = objek.position.y
        return (y, x)

    def isTaken(self, board: Board, x, y):
        for game_object in board.game_objects:
            if game_object.position.x == x and game_object.position.y == y and game_object.type != "DiamondGameObject":
                return True
        return False
    
    def isTeleportReset(self, board: Board,Goal: Position,Id: int):
        for objek in board.game_objects:
            if objek.type == "TeleportGameObject" and objek.id == Id:
                if objek.position.x != Goal.x and objek.position.y != Goal.y:
                    return True
                else:    
                    return False
                
    def next_move(self, board_bot: GameObject, board: Board):
        print("Goal Position: ", self.goal_position)
        props = board_bot.properties
        current_position = board_bot.position
        sessionlegth = props.milliseconds_left
        base_x = board_bot.properties.base.x
        base_y = board_bot.properties.base.y
        if self.isTeleport:
            print("Teleporting to: ", self.teleport)
            delta_x, delta_y = get_direction(current_position.x,current_position.y,self.teleport.x,self.teleport.y)
            if current_position.x + delta_x == self.teleport.x and current_position.y + delta_y == self.teleport.y:
                self.isTeleport = False
                self.teleport = None
                self.idTeleport = -1
            elif self.isTeleportReset(board, self.teleport, self.idTeleport):
                self.isTeleport = False
                self.teleport = None
                self.idTeleport = -1
            return delta_x, delta_y
    
        if self.goal_position == Position(base_y, base_x):
            print("Moving to base")
            if self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
                self.goal_position = None
            elif self.isTaken(board, self.goal_position.x, self.goal_position.y):
                self.goal_position = None
            temp = False
            for tele1 in board.game_objects:
                if tele1.type == "TeleportGameObject" :
                    for tele2 in board.game_objects:
                        if tele2.type == "TeleportGameObject" and tele2.id != tele1.id:
                            if self.countSteps(current_position, tele1.position) + self.countSteps(tele2.position, Position(base_y, base_x)) < self.countSteps(current_position, Position(base_y, base_x)):
                                self.teleport = Position(tele1.position.y, tele1.position.x)
                                self.isTeleport = True
                                self.idTeleport = tele1.id
                                temp = True
                                break
                    if temp:
                        break

        elif self.goal_position != None and self.goal_position != Position(base_y, base_x):
            if self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
                self.goal_position = None
            elif self.isTaken(board, self.goal_position.x, self.goal_position.y):
                self.goal_position = None
            else:
                temp = False
                for tele1 in board.game_objects:
                    if tele1.type == "TeleportGameObject" :
                        for tele2 in board.game_objects:
                            if tele2.type == "TeleportGameObject" and tele2.id != tele1.id:
                                if self.countSteps(current_position, tele1.position) + self.countSteps(tele2.position, self.goal_position) < self.countSteps(current_position, self.goal_position):
                                    self.teleport = Position(tele1.position.y, tele1.position.x)
                                    self.isTeleport = True
                                    self.idTeleport = tele1.id
                                    temp = True
                                    break
                        if temp:
                            break
            
        if sessionlegth < 10000 and props.diamonds > 2:
            # Move to base
            self.goal_position = Position(base_y, base_x)

        if self.goal_position == None:    
            check = self.NewCheckSekitar(board_bot, board)
            if props.diamonds == 5:
                # Move to base
                self.goal_position = Position(base_y, base_x)
            elif check[0] != -1:
                # Move to target
                self.goal_position = Position(check[0], check[1])
        
        if self.goal_position.x == -1 and self.goal_position.y == -1:
            for red in board.game_objects:
                if red.type == "RedGameObject":
                    self.goal_position = Position(red.position.y, red.position.x)
                    break
        return get_direction(current_position.x,current_position.y,self.goal_position.x,self.goal_position.y)