# Rôle :
# - Afficher vies
# - Dés
# - Score
# Toujours visible pendant la partie.

import pygame

class HUD: #Gère l'affichage de l'interface utilisateur pendant le jeu
    
    def __init__(self, largeur_ecran):
        self.largeur_ecran = largeur_ecran
        self.police_normale = pygame.font.Font(None, 28)
        self.police_petite = pygame.font.Font(None, 20)
        
        #Couleurs
        self.BLANC = (255, 255, 255)
        self.JAUNE = (255, 215, 0)
        self.GRIS = (50, 50, 70)
        self.GRIS_CLAIR = (100, 100, 120)
        self.ROUGE = (231, 76, 60)
    
    def afficher_liste_joueurs(self, ecran, joueurs, joueur_actuel_index): #Affiche la liste des joueurs sur le côté droit
        x = self.largeur_ecran - 270
        y = 20
        
        #Titre
        texte_titre = self.police_normale.render("JOUEURS", True, self.BLANC)
        ecran.blit(texte_titre, (x, y))
        y += 40
        
        # Afficher chaque joueur
        for i, joueur in enumerate(joueurs):
            #Fond
            couleur_fond = joueur.couleur if i == joueur_actuel_index else self.GRIS
            fond = pygame.Surface((250, 70))
            fond.fill(couleur_fond)
            fond.set_alpha(100)
            ecran.blit(fond, (x, y))
            
            #Bordure
            couleur_bordure = self.JAUNE if i == joueur_actuel_index else self.GRIS_CLAIR
            pygame.draw.rect(ecran, couleur_bordure, (x, y, 250, 70), 3)
            
            #Nom
            texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
            ecran.blit(texte_nom, (x + 10, y + 10))
            
            #Score
            texte_score = self.police_petite.render(f"Score: {joueur.score}", True, self.JAUNE)
            ecran.blit(texte_score, (x + 10, y + 35))
            
            #Vies
            couleur_vie = self.ROUGE if joueur.vies > 0 else self.GRIS_CLAIR
            texte_vies = self.police_petite.render(f"Vies: {joueur.vies}/10", True, couleur_vie)
            ecran.blit(texte_vies, (x + 140, y + 35))
            
            y += 80