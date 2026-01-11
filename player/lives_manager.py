# Rôle :
# - Initialisation des vies (ex : 10)
# - Perte de vie (porte, échec, solitude)
# - Vérifier si un joueur est éliminé

import pygame

class LivesManager: #Gère l'affichage des vies
    
    def __init__(self):
        self.police_normale = pygame.font.Font(None, 28)
        self.police_titre = pygame.font.Font(None, 36)
        
        #Couleurs
        self.ROUGE = (231, 76, 60)
        self.BLANC = (255, 255, 255)
        self.GRIS = (50, 50, 70)
        self.GRIS_VIDE = (70, 70, 70)
    
    def afficher_vies(self, ecran, joueur): #Affiche les vies du joueur sous forme de cœurs
        #Fond
        fond = pygame.Surface((360, 80))
        fond.fill(self.GRIS)
        pygame.draw.rect(fond, self.ROUGE, (0, 0, 360, 80), 4)
        ecran.blit(fond, (20, 160))
        
        #Nom du joueur
        texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
        ecran.blit(texte_nom, (30, 170))
        
        #Dessiner les 10 cœurs
        x_coeur = 30
        y_coeur = 205
        for i in range(10):
            if i < joueur.vies:
                #Cœur plein
                texte_coeur = self.police_titre.render("♥", True, self.ROUGE)
            else:
                #Cœur vide
                texte_coeur = self.police_titre.render("♥", True, self.GRIS_VIDE)
            
            ecran.blit(texte_coeur, (x_coeur, y_coeur))
            x_coeur += 35