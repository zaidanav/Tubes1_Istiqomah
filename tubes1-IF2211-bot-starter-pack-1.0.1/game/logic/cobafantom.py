
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class CobaFantom(BaseLogic):
    def __init__(self):
        # Inisialisasi variabel yang diperlukan
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Daftar arah pergerakan
        self.goal_position: Optional[Position] = None  # Posisi tujuan
        self.teleport: Optional[Position] = None  # Posisi teleporter yang dituju
        self.isTeleport = False  # Status apakah sedang melakukan teleportasi
        self.current_direction = 0  # Indeks arah saat ini dalam daftar arah
        self.idTeleport = -1  # ID teleporter yang dituju
        self.previous_goal: Optional[Position] = None  # Posisi tujuan sebelumnya

    def pythagoras(self, x1, y1, x2, y2):
        # Fungsi untuk menghitung jarak Euclidean antara dua titik
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

    def count_steps(self, goal: Position, current: Position):
        # Fungsi untuk menghitung jumlah langkah dari posisi saat ini ke posisi tujuan
        return abs(goal.x - current.x) + abs(goal.y - current.y)

    def count_diamonds(self, board: Board, center, rad):
        # Fungsi untuk menghitung jumlah berlian di sekitar pusat dengan radius tertentu
        count = 0
        range_xfirst = center.x - rad
        range_yfirst = center.y - rad
        range_xlast = center.x + rad
        range_ylast = center.y + rad
        for i in range(range_xfirst, range_xlast+1):
            for j in range(range_yfirst, range_ylast+1):
                if i < 0 or i >= board.width or j < 0 or j >= board.height:
                    continue
                for game_object in board.game_objects:
                    if game_object.position.x == i and game_object.position.y == j and game_object.type == "DiamondGameObject":
                        count += 1
        return count

    def find_nearest_diamond(self, board_bot: GameObject, board: Board):
        # Fungsi untuk mencari posisi berlian terdekat
        props = board_bot.properties
        current_position = board_bot.position
        nearest_distance = float('inf')
        nearest_diamond = None
        for objek in board.game_objects:
            if objek.type == "DiamondGameObject":
                cek = False
                for k in range(len(board.diamonds)):
                    if board.diamonds[k].position.x == objek.position.x and board.diamonds[k].position.y == objek.position.y and board.diamonds[k].properties.points + props.diamonds > 5:
                        cek = True
                if cek:
                    continue
                distance = self.pythagoras(current_position.x, current_position.y, objek.position.x, objek.position.y)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_diamond = objek
        if nearest_diamond:
            return nearest_diamond.position.y, nearest_diamond.position.x
        return -1, -1

    def find_nearest_object(self, board_bot: GameObject, board: Board, object_types):
        # Fungsi untuk mencari posisi objek terdekat berdasarkan jenis objek
        props = board_bot.properties
        current_position = board_bot.position
        nearest_distance = float('inf')
        nearest_object = None
        for objek in board.game_objects:
            if objek.type in object_types:
                if objek.type == "TeleportGameObject":
                    for tele in board.game_objects:
                        if tele.type == "TeleportGameObject" and tele.id != objek.id: 
                            if self.count_diamonds(board, tele.position, 5) < 5:
                                continue
                cek = False
                if objek.type == "DiamondGameObject":
                    for k in range(len(board.diamonds)):
                        if board.diamonds[k].position.x == objek.position.x and board.diamonds[k].position.y == objek.position.y and board.diamonds[k].properties.points + props.diamonds > 5:
                            cek = True
                if cek:
                    continue
                distance = self.pythagoras(current_position.x, current_position.y, objek.position.x, objek.position.y)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_object = objek
        if nearest_object:
            return nearest_object.position.y, nearest_object.position.x
        return -1, -1

    def is_object_teleport(self, board: Board, x, y):
        # Fungsi untuk mengecek apakah posisi tertentu adalah posisi teleporter
        for game_object in board.game_objects:
            if game_object.position.x == x and game_object.position.y == y and game_object.type == "TeleportGameObject":
                return True
        return False

    def is_taken(self, board: Board, x, y):
        # Fungsi untuk mengecek apakah posisi tertentu sudah ditempati oleh objek lain selain berlian
        for game_object in board.game_objects:
            if game_object.position.x == x and game_object.position.y == y and game_object.type != "DiamondGameObject":
                return True
        return False
    
    def is_teleport_reset(self, board: Board, goal: Position, id: int):
        # Fungsi untuk mengecek apakah posisi teleporter telah dikembalikan ke posisi semula
        for objek in board.game_objects:
            if objek.type == "TeleportGameObject" and objek.id == id:
                if objek.position.x != goal.x and objek.position.y != goal.y:
                    return True
                else:    
                    return False
    
    def next_move(self, board_bot: GameObject, board: Board):
        # Fungsi utama untuk menentukan langkah selanjutnya
        props = board_bot.properties
        current_position = board_bot.position
        session_length = props.milliseconds_left
        base_x = board_bot.properties.base.x
        base_y = board_bot.properties.base.y
        
        if self.isTeleport:
            # Jika sedang melakukan teleportasi, gerakkan ke posisi teleporter yang dituju
            delta_x, delta_y = get_direction(current_position.x, current_position.y, self.teleport.x, self.teleport.y)
            if current_position.x + delta_x == self.teleport.x and current_position.y + delta_y == self.teleport.y:
                # Jika sudah sampai di posisi teleporter, hentikan teleportasi
                self.isTeleport = False
                self.teleport = None
                self.idTeleport = -1
            elif self.is_teleport_reset(board, self.teleport, self.idTeleport):
                # Jika posisi teleporter telah kembali ke posisi semula, hentikan teleportasi
                self.isTeleport = False
                self.teleport = None
                self.idTeleport = -1
            return delta_x, delta_y
    
        if self.goal_position == Position(base_y, base_x):
            # Jika tujuan adalah base, gerakkan ke base
            if self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
                self.goal_position = None
            elif self.is_taken(board, self.goal_position.x, self.goal_position.y):
                self.goal_position = None
            temp = False
            for tele1 in board.game_objects:
                if tele1.type == "TeleportGameObject":
                    for tele2 in board.game_objects:
                        if tele2.type == "TeleportGameObject" and tele2.id != tele1.id:
                            if self.count_steps(current_position, tele1.position) + self.count_steps(tele2.position, Position(base_y, base_x)) < self.count_steps(current_position, Position(base_y, base_x)):
                                self.teleport = Position(tele1.position.y, tele1.position.x)
                                self.isTeleport = True
                                self.idTeleport = tele1.id
                                temp = True
                                break
                    if temp:
                        break

        elif self.goal_position and self.goal_position != Position(base_y, base_x):
            # Jika tujuan bukan base, cek apakah tujuan adalah teleporter yang menguntungkan
            if self.goal_position.x == board_bot.position.x and self.goal_position.y == board_bot.position.y:
                self.goal_position = None
            elif self.is_taken(board, self.goal_position.x, self.goal_position.y):
                self.goal_position = None
            else:
                temp = False
                for tele1 in board.game_objects:
                    if tele1.type == "TeleportGameObject":
                        for tele2 in board.game_objects:
                            if tele2.type == "TeleportGameObject" and tele2.id != tele1.id:
                                if self.count_steps(current_position, tele1.position) + self.count_steps(tele2.position, self.goal_position) < self.count_steps(current_position, self.goal_position):
                                    self.teleport = Position(tele1.position.y, tele1.position.x)
                                    self.isTeleport = True
                                    self.idTeleport = tele1.id
                                    temp = True
                                    break
                        if temp:
                            break
            
        if session_length < 10000 and props.diamonds > 2:
            # Jika tersisa waktu kurang dari 10 detik dan memiliki lebih dari 2 berlian, gerakkan ke base
            self.goal_position = Position(base_y, base_x)



        if not self.goal_position:
            # Jika tidak ada tujuan, cari tujuan baru
            if self.previous_goal:
                if self.is_object_teleport(board, self.previous_goal.x, self.previous_goal.y):
                    check = self.find_nearest_diamond(board_bot, board)
                else:
                    check = self.find_nearest_object(board_bot, board, ["DiamondGameObject", "TeleportGameObject"])
            else:
                check = self.find_nearest_object(board_bot, board, ["DiamondGameObject", "TeleportGameObject"])
            
            if props.diamonds == 5:
                # Jika jumlah berlian adalah 5, gerakkan ke base
                self.goal_position = Position(base_y, base_x)
                self.previous_goal = Position(base_y, base_x)

            elif props.diamonds == 3:
                # Jika jumlah berlian adalah 3, periksa apakah tujuan lebih dekat daripada base
                if self.count_steps(current_position, Position(check[0], check[1])) <= self.count_steps(current_position, board_bot.properties.base):
                    self.goal_position = Position(check[0], check[1])
                    self.previous_goal = Position(check[0], check[1])
                    return get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
                else:  
                    self.goal_position = Position(base_y, base_x)
                    self.previous_goal = Position(base_y, base_x)
                    return get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            elif check[0] != -1:
                # Jika ada tujuan yang ditemukan, gerakkan ke tujuan
                self.goal_position = Position(check[0], check[1])
                self.previous_goal = Position(check[0], check[1])
                return get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)

            else:
                # Jika tidak ada tujuan yang ditemukan, jelajahi peta
                if current_position.x >= board.width - 1:
                    self.current_direction = 1
                elif current_position.x <= 0:
                    self.current_direction = 0
                if current_position.y >= board.height - 1:
                    self.current_direction = 3
                elif current_position.y <= 0:
                    self.current_direction = 2

                for i in range(4):
                    x, y = current_position.x + self.directions[self.current_direction][0], current_position.y + self.directions[self.current_direction][1]
                    if not (x < 0 or x >= board.width or y < 0 or y >= board.height or self.is_taken(board, x, y)):
                        self.goal_position = Position(y, x)
                        self.previous_goal = Position(y, x)
                        return self.directions[self.current_direction]
                    else:
                        self.current_direction = (self.current_direction + 1) % 4
        
        return get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)


