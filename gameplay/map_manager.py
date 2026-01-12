import random

COULEURS_SALLES = {
    "B": (52, 152, 219),
    "V": (46, 204, 113),
    "R": (231, 76, 60),
    "J": (241, 196, 15)
}

class MapManager:
    def __init__(self):
        self.grid_size = 3
        self.grid = []
        self.player_pos = [1, 1] # Départ au centre (B2)
        self.exit_pos = [0, 0]
        
        # Système de quêtes pour la fin
        self.quests_completed = 0
        self.min_quests_to_exit = 2 # Il faut réussir 2 énigmes pour voir la sortie
        self.exit_revealed = False
        
        self.generate_new_map()

    def generate_new_map(self):
        colors = ["B", "V", "R", "J"]
        self.grid = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                row.append(random.choice(colors))
            self.grid.append(row)
            
        self.player_pos = [1, 1] 
        self.quests_completed = 0
        self.exit_revealed = False
        
        # Sortie aléatoire différente du départ
        while True:
            ex = random.randint(0, 2)
            ey = random.randint(0, 2)
            if [ex, ey] != self.player_pos:
                self.exit_pos = [ex, ey]
                break

    def check_exit_condition(self):
        """Vérifie si la sortie doit apparaître"""
        if self.quests_completed >= self.min_quests_to_exit:
            self.exit_revealed = True

    def get_current_room_color(self):
        x, y = self.player_pos
        code = self.grid[y][x]
        return COULEURS_SALLES[code]

    def get_coordinates_str(self, x, y):
        """Convertit (0,0) en 'A1', (1,2) en 'B3'"""
        lettres = ["A", "B", "C"]
        chiffres = ["1", "2", "3"]
        return f"{lettres[x]}{chiffres[y]}"

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == "HAUT": dy = -1
        elif direction == "BAS": dy = 1
        elif direction == "GAUCHE": dx = -1
        elif direction == "DROITE": dx = 1
        
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.player_pos = [new_x, new_y]
            return True
        return False