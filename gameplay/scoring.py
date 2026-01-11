# Gère le système de score.
# Rôle :
# - Récompense la coopération
# - Pénalise les erreurs

import pygame

class ScoringSystem: #Gère le calcul et l'affichage des scores
    
    def __init__(self):
        self.police_titre = pygame.font.Font(None, 36)
        self.police_normale = pygame.font.Font(None, 28)
        self.police_petite = pygame.font.Font(None, 20)
        
        # Couleurs
        self.JAUNE = (255, 215, 0)
        self.BLANC = (255, 255, 255)
        self.GRIS = (50, 50, 70)
        self.GRIS_CLAIR = (100, 100, 120)
    
    def calculer_score_equipe(self, joueurs): #Calcule le score TOTAL de tous les joueurs
        score_total = 0
        for joueur in joueurs:
            score_total += joueur.score
        return score_total
    
    def afficher_hud_score(self, ecran, joueurs, joueur_actuel_index): #Affiche le HUD du score en haut à gauche
        #Fond noir
        fond = pygame.Surface((250, 120))
        fond.fill(self.GRIS)
        pygame.draw.rect(fond, self.JAUNE, (0, 0, 250, 120), 4)
        ecran.blit(fond, (20, 20))
        
        #Score équipe
        texte_label = self.police_petite.render("SCORE ÉQUIPE", True, self.GRIS_CLAIR)
        ecran.blit(texte_label, (30, 30))
        
        score_equipe = self.calculer_score_equipe(joueurs)
        texte_score = self.police_titre.render(str(score_equipe), True, self.JAUNE)
        ecran.blit(texte_score, (30, 50))
        
        #Ligne séparation
        pygame.draw.line(ecran, self.GRIS_CLAIR, (30, 90), (260, 90), 2)
        
        #Score individuel
        texte_ton_score = self.police_petite.render("TON SCORE", True, self.GRIS_CLAIR)
        ecran.blit(texte_ton_score, (30, 95))
        
        joueur = joueurs[joueur_actuel_index]
        texte_score_perso = self.police_normale.render(str(joueur.score), True, self.BLANC)
        ecran.blit(texte_score_perso, (30, 115))
    
    def recompenser_enigme_reussie(self, joueur):
        joueur.gagner_points(100)
    
    def penaliser_enigme_ratee(self, joueur):
        joueur.perdre_vie()