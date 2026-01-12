# Rôle :
# - Initialisation des vies (ex : 10)
# - Perte de vie (porte, échec, solitude)
# - Vérifier si un joueur est éliminé

import pygame

class LivesManager: # Gère l'affichage des vies
    
    def __init__(self):
        self.police_normale = pygame.font.Font(None, 28)
        self.police_titre = pygame.font.Font(None, 36)
        
        #Couleurs
        self.ROUGE = (231, 76, 60)
        self.BLANC = (255, 255, 255)
        self.GRIS = (50, 50, 70)
        self.GRIS_VIDE = (70, 70, 70)
    
    def afficher_vies(self, ecran, joueur): # Affiche les vies du joueur sous forme de cœurs
        
        # Nouvelle Position et Taille
        # Le Score finit à Y=200, donc on se place à Y=210 avec une marge
        x_pos = 20
        y_pos = 210 
        width = 250  # Réduit de 360 à 250 pour s'aligner avec le Score
        height = 70  # Légèrement plus petit
        
        # Fond
        fond = pygame.Surface((width, height))
        fond.fill(self.GRIS)
        ecran.blit(fond, (x_pos, y_pos))
        
        # Nom du joueur
        texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
        ecran.blit(texte_nom, (x_pos + 10, y_pos + 10))
        
        # Texte chiffré (ex: 8/10) à droite
        texte_chiffre = self.police_normale.render(f"{joueur.vies}/10", True, self.ROUGE)
        ecran.blit(texte_chiffre, (x_pos + width - 60, y_pos + 10))
        
        # Dessiner les 10 cœurs (Resserrés)
        x_coeur = x_pos + 10
        y_coeur = y_pos + 35
        
        for i in range(10):
            if i < joueur.vies:
                # Cœur plein
                # J'utilise un caractère unicode simple ou la police normale pour que ça rentre
                texte_coeur = self.police_normale.render("♥", True, self.ROUGE)
            else:
                # Cœur vide
                texte_coeur = self.police_normale.render("♡", True, self.GRIS_VIDE)
            
            ecran.blit(texte_coeur, (x_coeur, y_coeur))
            
            # On réduit l'espacement entre les cœurs (23 pixels au lieu de 35)
            x_coeur += 23