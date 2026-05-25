import pygame
import random

class Dice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rolling = False
        self.result = 1
        self.final_result = 1
        self.color = (255, 50, 50)
        self.frames_left = 0
        self.update_delay = 2
        self.frame_counter = 0
        self.text_font = pygame.font.SysFont(None, 30) # Taille ajustée pour la lisibilité
        self.selected_players = []
        self.target_room = ""

    def roll(self, final_result, selected_players, target_room):
        self.rolling = True
        self.frames_left = 120  
        self.final_result = final_result
        self.selected_players = selected_players
        self.target_room = target_room
        self.update_delay = 2 
        self.frame_counter = 0

    def update(self, total_players):
        if self.rolling:
            self.frames_left -= 1
            self.frame_counter += 1

            if self.frames_left < 60: self.update_delay = 4
            if self.frames_left < 30: self.update_delay = 8
            if self.frames_left < 10: self.update_delay = 15

            if self.frame_counter >= self.update_delay:
                self.frame_counter = 0
                self.result = random.randint(1, min(6, max(1, total_players)))
                if total_players > 6 and random.random() < 0.15: self.result = "+"
                self._update_color()

            if self.frames_left <= 0:
                self.rolling = False
                self.result = self.final_result 
                self._update_color()
                return self.result
        return None

    def _update_color(self):
        val = self.result if isinstance(self.result, int) else 4
        if val == 1: self.color = (220, 20, 60)    
        elif val == 2: self.color = (30, 144, 255) 
        elif val == 3: self.color = (50, 205, 50)  
        else: self.color = (255, 215, 0)           

    def draw(self, ecran):
        offset_y = random.randint(-10, 10) if self.rolling else 0
        rect = pygame.Rect(self.x - 45, self.y - 45 + offset_y, 90, 90)
        
        if self.rolling:
            pulse = random.randint(-5, 5)
            rect.inflate_ip(pulse, pulse)

        pygame.draw.rect(ecran, self.color, rect, border_radius=14)
        pygame.draw.rect(ecran, (255, 255, 255), rect, 3, border_radius=14)
        
        cx, cy = rect.center
        
        if self.result == "+":
            pygame.draw.line(ecran, (255, 255, 255), (cx - 18, cy), (cx + 18, cy), 6)
            pygame.draw.line(ecran, (255, 255, 255), (cx, cy - 18), (cx, cy + 18), 6)
        elif isinstance(self.result, int):
            r = 7 
            dots = []
            if self.result in [1, 3, 5]: dots.append((cx, cy))
            if self.result in [2, 3, 4, 5, 6]:
                dots.append((cx - 22, cy - 22))
                dots.append((cx + 22, cy + 22))
            if self.result in [4, 5, 6]:
                dots.append((cx + 22, cy - 22))
                dots.append((cx - 22, cy + 22))
            if self.result == 6:
                dots.append((cx - 22, cy))
                dots.append((cx + 22, cy))
                
            for d in dots: pygame.draw.circle(ecran, (255, 255, 255), d, r)

    def draw_selection_ui(self, ecran, largeur):
        if not self.rolling and self.selected_players:
            noms = ", ".join([p.nom for p in self.selected_players])
            # CORRECTION : Remplacement de la flèche unicode problématique par ->
            txt = self.text_font.render(f"DESIGNES : {noms}  ->  REJOINDRE : {self.target_room}", True, (255, 255, 255))
            
            # Positionnement sous la barre de vie supérieure pour éviter toute collision
            txt_rect = txt.get_rect(center=(largeur // 2, 95))
            bg_rect = txt_rect.inflate(30, 15)
            pygame.draw.rect(ecran, (10, 15, 25), bg_rect, border_radius=6)
            pygame.draw.rect(ecran, (255, 255, 255), bg_rect, 1, border_radius=6)
            ecran.blit(txt, txt_rect)