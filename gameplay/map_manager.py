import random
import pygame
import os

COULEURS_SALLES = {
    "G": (35, 35, 45),       
    "A": (39, 174, 96),      
    "L": (41, 128, 185),     
    "O": (241, 196, 15)      
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
            "L": "assets/sol_labo.png",
            "O": "assets/sol_salle_jaune.png"
        }
        
        for theme_code, path in image_paths.items():
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                self.backgrounds[theme_code] = pygame.transform.scale(img, (1000, 700))
            else:
                surf = pygame.Surface((1000, 700))
                surf.fill(COULEURS_SALLES[theme_code])
                self.backgrounds[theme_code] = surf
        
        self.generate_new_map()

    def generate_new_map(self):
        salles = ["A", "L", "O", "G", "G", "G", "G", "G", "G"]
        while True:
            random.shuffle(salles)
            if salles[4] == "G": break
                
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
            ex, ey = random.randint(0, 2), random.randint(0, 2)
            if [ex, ey] != self.player_pos:
                self.exit_pos = [ex, ey]
                break

    def check_exit_condition(self):
        if self.quests_completed >= self.min_quests_to_exit and not self.exit_revealed:
            self.exit_revealed = True
            while self.exit_pos == self.player_pos:
                self.exit_pos = [random.randint(0, 2), random.randint(0, 2)]

    def get_current_room_type(self):
        return self.grid[self.player_pos[1]][self.player_pos[0]]

    def draw(self, screen):
        screen.blit(self.backgrounds[self.get_current_room_type()], (0, 0))