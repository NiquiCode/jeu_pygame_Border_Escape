import random
import pygame

# "G": Grotte, "A": Acide, "L": Labo
COULEURS_SALLES = {
    "G": (30, 30, 30),
    "A": (46, 204, 113),
    "L": (52, 152, 219)
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
        
        # Association des thèmes aux images
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
                # Double sécurité pour la grotte si elle s'appelle différemment
                if theme_code == "G":
                    try:
                        img = pygame.image.load("assets/sol_grotte_pixel.png").convert()
                        self.backgrounds[theme_code] = pygame.transform.scale(img, (1000, 700))
                        continue
                    except:
                        pass
                        
                # Fond de secours si introuvable
                surf = pygame.Surface((1000, 700))
                r, g, b = COULEURS_SALLES[theme_code]
                surf.fill((max(0, r-50), max(0, g-50), max(0, b-50)))
                self.backgrounds[theme_code] = surf
        
        self.generate_new_map()

    def generate_new_map(self):
        salles = ["A", "L", "G", "G", "G", "G", "G", "G", "G"]
        
        # --- NOUVEAU : On s'assure que le joueur spawn dans une Grotte ---
        # L'index 4 correspond au centre (B2) de la grille 3x3
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
        
        # Position initiale de la sortie (sera re-vérifiée plus tard)
        while True:
            ex = random.randint(0, 2)
            ey = random.randint(0, 2)
            if [ex, ey] != self.player_pos:
                self.exit_pos = [ex, ey]
                break

    def check_exit_condition(self):
        # --- NOUVEAU : La sortie s'éloigne du joueur si besoin ---
        if self.quests_completed >= self.min_quests_to_exit and not self.exit_revealed:
            self.exit_revealed = True
            
            # Si la sortie pré-calculée est dans la même salle que le joueur, on la déplace
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