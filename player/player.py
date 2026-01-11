# Rôle :
# - Déplacements
# - Interactions avec l’environnement
# - Entrée dans les salles

import pygame

class Joueur:
    """Classe qui gère un joueur: nom,vies,score,position"""
    
    def __init__(self, nom, couleur, position_spawn=(100, 100)):
        self.nom = nom
        self.vies = 10  # 10 vies au départ
        self.score = 0
        self.couleur = couleur
        self.x = position_spawn[0]
        self.y = position_spawn[1]
        self.taille = 40
        self.vitesse = 5
    
    def gagner_points(self, points):
        self.score += points
    
    def perdre_vie(self):
        if self.vies > 0:
            self.vies -= 1
    
    def est_vivant(self):
        return self.vies > 0
    
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def dessiner(self, ecran):
        """Dessiner le joueur sur l'écran"""
        pygame.draw.rect(ecran, self.couleur, 
                        (self.x, self.y, self.taille, self.taille))
        pygame.draw.rect(ecran, (190, 255, 190), 
                        (self.x, self.y, self.taille, self.taille), 3)