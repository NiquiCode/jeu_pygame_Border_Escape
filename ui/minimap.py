import pygame
from gameplay.map_manager import COULEURS_SALLES

class Minimap:
    def __init__(self, screen_width, screen_height, map_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_manager = map_manager
        
        self.show_big = False 
        self.font = pygame.font.Font(None, 30)

    def toggle(self):
        self.show_big = not self.show_big

    def draw(self, screen):
        # Configuration Taille et Position
        if self.show_big:
            case_size = 150
            margin = 20
            # Centre
            start_x = (self.screen_width - (case_size * 3)) // 2
            start_y = (self.screen_height - (case_size * 3)) // 2
            alpha = 230
        else:
            case_size = 40
            margin = 5
            # BAS GAUCHE
            start_x = 40 
            start_y = self.screen_height - (case_size * 3) - 40
            alpha = 180

        bg_w = case_size * 3 + margin * 4
        bg_h = case_size * 3 + margin * 4
        
        map_surface = pygame.Surface((bg_w, bg_h))
        map_surface.set_alpha(alpha)
        map_surface.fill((20, 20, 30))
        
        grid = self.map_manager.grid
        px, py = self.map_manager.player_pos
        ex, ey = self.map_manager.exit_pos
        
        # Dessin des labels (A, B, C / 1, 2, 3)
        lettres = ["A", "B", "C"]
        chiffres = ["1", "2", "3"]

        for y in range(3):
            # Dessin Chiffres (1, 2, 3) à gauche
            if self.show_big:
                lbl = self.font.render(chiffres[y], True, (255, 255, 255))
                screen.blit(lbl, (start_x - 30, start_y + y*(case_size+5) + case_size//2))

            for x in range(3):
                # Dessin Lettres (A, B, C) en haut (seulement sur la première ligne)
                if y == 0 and self.show_big:
                    lbl = self.font.render(lettres[x], True, (255, 255, 255))
                    screen.blit(lbl, (start_x + x*(case_size+5) + case_size//2, start_y - 30))

                code = grid[y][x]
                color = COULEURS_SALLES[code]
                
                rect_x = x * (case_size + 5) + 10
                rect_y = y * (case_size + 5) + 10
                rect = pygame.Rect(rect_x, rect_y, case_size, case_size)
                
                pygame.draw.rect(map_surface, color, rect, border_radius=4)
                
                # Joueur
                if x == px and y == py:
                    pygame.draw.circle(map_surface, (255, 255, 255), rect.center, case_size // 5)
                
                # Sortie (Seulement si révélée !)
                if x == ex and y == ey and self.map_manager.exit_revealed:
                     door_rect = pygame.Rect(0, 0, case_size//3, case_size//2)
                     door_rect.center = rect.center
                     pygame.draw.rect(map_surface, (50, 25, 0), door_rect)

        if self.show_big:
            pygame.draw.rect(map_surface, (255, 255, 255), map_surface.get_rect(), 2)
            
        screen.blit(map_surface, (start_x, start_y))