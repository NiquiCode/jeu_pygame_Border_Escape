import pygame

class HUD:
    def __init__(self, largeur_ecran):
        self.largeur_ecran = largeur_ecran
        self.police_normale = pygame.font.Font(None, 26)
        self.police_petite = pygame.font.Font(None, 20)
        
        self.BLANC = (255, 255, 255)
        self.JAUNE = (255, 215, 0)
        self.GRIS = (25, 25, 35)
        self.GRIS_CLAIR = (120, 120, 140)
        self.ROUGE = (231, 76, 60)
    
    def afficher_liste_joueurs(self, ecran, joueurs, joueur_actuel_index):
        # Positionnement sur le côté droit sans empiéter sur le centre
        x = self.largeur_ecran - 270
        y = 20
        
        texte_titre = self.police_normale.render("SURVIVANTS", True, self.BLANC)
        ecran.blit(texte_titre, (x, y))
        y += 35
        
        for i, joueur in enumerate(joueurs):
            # Conteneur individuel propre
            fond = pygame.Surface((250, 60), pygame.SRCALPHA)
            fond.fill((30, 35, 45, 220)) 
            ecran.blit(fond, (x, y))
            
            # Bordure distinctive pour le joueur dont c'est le tour
            couleur_bordure = self.JAUNE if i == joueur_actuel_index else self.GRIS_CLAIR
            epaisseur = 2 if i == joueur_actuel_index else 1
            pygame.draw.rect(ecran, couleur_bordure, (x, y, 250, 60), epaisseur, border_radius=4)
            
            # Nom de l'utilisateur
            texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
            ecran.blit(texte_nom, (x + 15, y + 8))
            
            # Informations de jeu alignées
            texte_score = self.police_petite.render(f"Pts: {joueur.score}", True, self.JAUNE)
            ecran.blit(texte_score, (x + 15, y + 34))
            
            couleur_vie = self.ROUGE if joueur.vies > 2 else self.GRIS_CLAIR
            texte_vies = self.police_petite.render(f"Vies: {joueur.vies}/10", True, couleur_vie)
            ecran.blit(texte_vies, (x + 140, y + 34))
            
            y += 70