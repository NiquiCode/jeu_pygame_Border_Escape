import pygame
import os

class LivesManager:
    def __init__(self):
        self.heart_full = self.load_img("assets/heart_full.png")
        self.heart_empty = self.load_img("assets/heart_empty.png")

    def load_img(self, path):
        if os.path.exists(path):
            return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (30, 30))
        surf = pygame.Surface((30, 30))
        surf.fill((255, 0, 0) if "full" in path else (100, 100, 100))
        return surf

    def afficher_vies(self, ecran, joueur):
        # Calcul de la position (en haut à droite)
        largeur = ecran.get_width()
        box_width = 10 * 35 + 20
        box_x = largeur - box_width - 20
        box_y = 20
        
        # Dessin du bloc de fond (transparent)
        fond = pygame.Surface((box_width, 50), pygame.SRCALPHA)
        fond.fill((20, 25, 35, 200)) # Noir bleuté transparent
        ecran.blit(fond, (box_x, box_y))
        
        # Bordure du bloc
        pygame.draw.rect(ecran, (200, 50, 50), (box_x, box_y, box_width, 50), 2, border_radius=5)
        
        # Dessin des cœurs à l'intérieur
        for i in range(10): 
            img = self.heart_full if i < joueur.vies else self.heart_empty
            ecran.blit(img, (box_x + 10 + i * 35, box_y + 10))