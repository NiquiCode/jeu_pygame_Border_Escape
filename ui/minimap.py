import pygame
from gameplay.map_manager import COULEURS_SALLES

class Minimap:
    def __init__(self, screen_width, screen_height, map_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_manager = map_manager
        
        self.show_big = False 
        self.font = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 18) # Pour la petite minimap

    def toggle(self):
        self.show_big = not self.show_big

    def draw(self, screen):
        # Configuration Taille et Position
        if self.show_big:
            case_size = 150
            margin = 35 # Marge agrandie pour laisser de la place aux lettres
            # Centre
            start_x = (self.screen_width - (case_size * 3 + margin * 2)) // 2
            start_y = (self.screen_height - (case_size * 3 + margin * 2)) // 2
            alpha = 230
            current_font = self.font
            offset_text = 20
        else:
            case_size = 40
            margin = 25 # Marge pour les petites lettres
            # BAS GAUCHE
            start_x = 20 
            start_y = self.screen_height - (case_size * 3 + margin * 2) - 20
            alpha = 180
            current_font = self.font_small
            offset_text = 12

        # La surface englobe les cases ET la zone pour le texte
        bg_w = case_size * 3 + margin + 15
        bg_h = case_size * 3 + margin + 15
        
        map_surface = pygame.Surface((bg_w, bg_h))
        map_surface.set_alpha(alpha)
        map_surface.fill((20, 20, 30))
        
        grid = self.map_manager.grid
        px, py = self.map_manager.player_pos
        ex, ey = self.map_manager.exit_pos
        
        lettres = ["A", "B", "C"]
        chiffres = ["1", "2", "3"]

        for y in range(3):
            # --- DESSIN DES CHIFFRES (1, 2, 3) SUR LA GAUCHE ---
            lbl = current_font.render(chiffres[y], True, (200, 200, 200))
            # On le centre verticalement par rapport à sa case
            text_y = margin + y * (case_size + 5) + (case_size // 2) - (lbl.get_height() // 2)
            map_surface.blit(lbl, (offset_text - lbl.get_width()//2, text_y))

            for x in range(3):
                # --- DESSIN DES LETTRES (A, B, C) EN HAUT ---
                if y == 0:
                    lbl_lettre = current_font.render(lettres[x], True, (200, 200, 200))
                    # On le centre horizontalement par rapport à sa case
                    text_x = margin + x * (case_size + 5) + (case_size // 2) - (lbl_lettre.get_width() // 2)
                    map_surface.blit(lbl_lettre, (text_x, offset_text - lbl_lettre.get_height()//2))

                # --- DESSIN DES CASES ---
                code = grid[y][x]
                color = COULEURS_SALLES[code]
                
                # On décale les cases de 'margin' pour laisser de la place au texte
                rect_x = margin + x * (case_size + 5)
                rect_y = margin + y * (case_size + 5)
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

        # Bordure autour de la minimap
        if self.show_big:
            pygame.draw.rect(map_surface, (255, 255, 255), map_surface.get_rect(), 2)
        else:
            pygame.draw.rect(map_surface, (100, 100, 100), map_surface.get_rect(), 1)
            
        screen.blit(map_surface, (start_x, start_y))