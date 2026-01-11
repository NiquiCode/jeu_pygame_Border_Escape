# Écran de fin de jeu.
# Rôle :
# - Victoire ou défaite
# - Message final
# - Retour au menu

import pygame

class EndScreen: #Gère l'écran de fin de partie avec classement
    
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.police_titre = pygame.font.Font(None, 36)
        self.police_normale = pygame.font.Font(None, 28)
        self.police_petite = pygame.font.Font(None, 20)
        
        #Couleurs
        self.NOIR = (0, 0, 0)
        self.BLANC = (255, 255, 255)
        self.JAUNE = (255, 215, 0)
        self.GRIS = (50, 50, 70)
        self.GRIS_CLAIR = (100, 100, 120)
    
    def afficher(self, ecran, joueurs): #Affiche l'écran de fin avec le classement
        #Fond semi-transparent
        fond = pygame.Surface((self.largeur, self.hauteur))
        fond.fill(self.NOIR)
        fond.set_alpha(230)
        ecran.blit(fond, (0, 0))
        
        #Titre
        texte_titre = self.police_titre.render("🏆 MISSION TERMINÉE 🏆", True, self.JAUNE)
        rect_titre = texte_titre.get_rect(center=(self.largeur // 2, 100))
        ecran.blit(texte_titre, rect_titre)
        
        #Score collectif
        score_total = sum(j.score for j in joueurs)
        texte_label = self.police_petite.render("SCORE COLLECTIF", True, self.GRIS_CLAIR)
        rect_label = texte_label.get_rect(center=(self.largeur // 2, 180))
        ecran.blit(texte_label, rect_label)
        
        texte_score = self.police_titre.render(str(score_total), True, self.JAUNE)
        rect_score = texte_score.get_rect(center=(self.largeur // 2, 220))
        ecran.blit(texte_score, rect_score)
        
        #Trier les joueurs
        joueurs_tries = sorted(joueurs, key=lambda j: j.score, reverse=True)
        
        #Afficher classement
        y = 300
        medailles = ["🥇", "🥈", "🥉"]
        
        for i, joueur in enumerate(joueurs_tries):
            #Fond
            couleur_fond = (100, 80, 0) if i == 0 else self.GRIS
            fond_joueur = pygame.Surface((600, 70))
            fond_joueur.fill(couleur_fond)
            ecran.blit(fond_joueur, (self.largeur // 2 - 300, y))
            
            #Bordure
            couleur_bordure = self.JAUNE if i == 0 else self.GRIS_CLAIR
            pygame.draw.rect(ecran, couleur_bordure, 
                           (self.largeur // 2 - 300, y, 600, 70), 3)
            
            #Médaille
            medaille = medailles[i] if i < 3 else f"{i+1}"
            texte_rang = self.police_titre.render(medaille, True, self.BLANC)
            ecran.blit(texte_rang, (self.largeur // 2 - 280, y + 15))
            
            #Nom
            couleur_nom = self.JAUNE if i == 0 else self.BLANC
            texte_nom = self.police_normale.render(joueur.nom, True, couleur_nom)
            ecran.blit(texte_nom, (self.largeur // 2 - 220, y + 20))
            
            #Score
            texte_score = self.police_normale.render(str(joueur.score), True, self.JAUNE)
            ecran.blit(texte_score, (self.largeur // 2 + 150, y + 20))
            
            #Vies
            texte_vies = self.police_petite.render(f"{joueur.vies} vies", True, self.GRIS_CLAIR)
            ecran.blit(texte_vies, (self.largeur // 2 + 50, y + 25))
            
            y += 80
        
        #Instructions
        texte_rejouer = self.police_petite.render("Appuyez sur R pour REJOUER", True, self.BLANC)
        rect_rejouer = texte_rejouer.get_rect(center=(self.largeur // 2, self.hauteur - 50))
        ecran.blit(texte_rejouer, rect_rejouer)