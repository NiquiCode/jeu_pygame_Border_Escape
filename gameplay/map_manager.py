import random
import pygame

COULEURS_SALLES = {
    "G": (35, 35, 45),       # Grotte (Gris sombre)
    "A": (39, 174, 96),      # Acide (Vert toxique bien visible)
    "L": (41, 128, 185)      # Labo (Bleu électrique intense)
}

class MapManager:
    def __init__(self):
        self.grid_size = 3
        self.grid = []
        self.player_pos = [1, 1] 
        self.exit_pos = [0, 0]
        
        self.quests_completed = 0
        self.min_quests_to_exit = 2 
        self.exit_revealed = False
        self.backgrounds = {}
        
        image_paths = {
            "G": "assets/sol.png",
            "A": "assets/sol_acide.png",
            "L": "assets/sol_labo.png"
        }
        
        for theme_code, path in image_paths.items():
            try:
                img = pygame.image.load(path).convert()
                self.backgrounds[theme_code] = pygame.transform.scale(img, (1000, 700))
            except FileNotFoundError:
                # Fallback haute visibilité si l'image est manquante
                surf = pygame.Surface((1000, 700))
                surf.fill(COULEURS_SALLES[theme_code])
                self.backgrounds[theme_code] = surf
        
        self.generate_new_map()

    def generate_new_map(self):
        salles = ["A", "L", "G", "G", "G", "G", "G", "G", "G"]
        
        while True:
            random.shuffle(salles)
            if salles[4] == "G": 
                break
                
        self.grid = []
        index = 0
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                row.append(salles[index])
                index += 1
            self.grid.append(row)
            
        self.player_pos = [1, 1] 
        self.quests_completed = 0
        self.exit_revealed = False
        
        while True:
            ex = random.randint(0, 2)
            ey = random.randint(0, 2)
            if [ex, ey] != self.player_pos:
                self.exit_pos = [ex, ey]
                break

    def check_exit_condition(self):
        if self.quests_completed >= self.min_quests_to_exit and not self.exit_revealed:
            self.exit_revealed = True
            while self.exit_pos == self.player_pos:
                self.exit_pos = [random.randint(0, 2), random.randint(0, 2)]

    def get_current_room_type(self):
        x, y = self.player_pos
        return self.grid[y][x]

    def get_current_room_color(self):
        code = self.get_current_room_type()
        return COULEURS_SALLES[code]

    def get_coordinates_str(self, x, y):
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
        
    def draw(self, screen):
        current_theme = self.get_current_room_type()
        screen.blit(self.backgrounds[current_theme], (0, 0))