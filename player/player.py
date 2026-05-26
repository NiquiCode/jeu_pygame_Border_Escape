import pygame
import os

class Player:
    def __init__(self, nom, couleur, player_id, is_local=False, x=100, y=100, image_path=None):
        self.nom = nom
        self.couleur = couleur
        self.player_id = player_id
        self.is_local = is_local
        self.x = x
        self.y = y
        self.speed = 4
        self.size = 120  
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.score = 0
        self.vies = 10
        self.indices_restants = 3
        self.facing_right = True
        self.is_host = False
        self.est_bloque = False
        self.is_selected = False
        self.room_pos = [1, 1]
        self.image_path = image_path
        self.image = None
        self.charger_image()

    def charger_image(self):
        if self.image_path and os.path.exists(self.image_path):
            try:
                img = pygame.image.load(self.image_path).convert_alpha()
                self.image = pygame.transform.scale(img, (self.size, self.size))
            except:
                self.image = None

    def reset(self):
        self.score = 0
        self.vies = 10
        self.indices_restants = 3
        self.est_bloque = False
        self.is_selected = False

    def gagner_points(self, points):
        self.score += points
        
    def perdre_points(self, points):
        self.score = max(0, self.score - points)
        
    def perdre_vie(self):
        self.vies -= 1

    def move(self, dx, dy, min_x, max_x, min_y, max_y):
        if self.est_bloque: return
        self.x = max(min_x, min(self.x + dx, max_x - self.size))
        self.y = max(min_y, min(self.y + dy, max_y - self.size))
        self.rect.topleft = (self.x, self.y)
        if dx != 0: self.facing_right = dx > 0
    
    def update(self):
        self.rect.topleft = (self.x, self.y)

    def update_from_dict(self, data):
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.score = data.get("score", self.score)
        self.vies = data.get("vies", self.vies)
        self.indices_restants = data.get("indices_restants", self.indices_restants)
        self.est_bloque = data.get("est_bloque", self.est_bloque)
        self.room_pos = data.get("room_pos", self.room_pos)
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen, font, actif=False):
        if self.image:
            img = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.couleur, self.rect, border_radius=8)
            if actif: pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)
        
        txt = font.render(self.nom, True, (255, 255, 0) if actif else (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(self.x + self.size // 2, self.y - 15)))
        
        if self.est_bloque:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + self.size, self.y + self.size), 4)
            pygame.draw.line(screen, (255, 0, 0), (self.x + self.size, self.y), (self.x, self.y + self.size), 4)