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
        # Gère le système de score.
# Rôle :
# - Récompense la coopération
# - Pénalise les erreurs
# - Affiche les Scores et les Quêtes

import pygame

class ScoringSystem: 
    
    def __init__(self):
        self.police_titre = pygame.font.Font(None, 36)
        self.police_normale = pygame.font.Font(None, 28)
        self.police_petite = pygame.font.Font(None, 20)
        
        # Couleurs
        self.JAUNE = (255, 215, 0)
        self.BLANC = (255, 255, 255)
        self.GRIS = (50, 50, 70)
        self.GRIS_CLAIR = (100, 100, 120)
        self.CYAN = (0, 255, 255)
    
    def calculer_score_equipe(self, joueurs): 
        score_total = 0
        for joueur in joueurs:
            score_total += joueur.score
        return score_total
    
    def afficher_hud_score(self, ecran, joueurs, joueur_actuel_index, map_manager): 
        """
        Affiche le HUD complet : Score Équipe, Score Perso et Progression Quêtes
        """
        # Fond plus grand (hauteur passée de 120 à 180 pour faire de la place)
        fond = pygame.Surface((250, 180))
        fond.fill(self.GRIS)
        pygame.draw.rect(fond, self.JAUNE, (0, 0, 250, 180), 3)
        ecran.blit(fond, (20, 20))
        
        # --- 1. Score Équipe ---
        texte_label = self.police_petite.render("SCORE ÉQUIPE", True, self.GRIS_CLAIR)
        ecran.blit(texte_label, (30, 30))
        
        score_equipe = self.calculer_score_equipe(joueurs)
        texte_score = self.police_titre.render(str(score_equipe), True, self.JAUNE)
        ecran.blit(texte_score, (30, 50))
        
        # Ligne séparation
        pygame.draw.line(ecran, self.GRIS_CLAIR, (30, 85), (250, 85), 1)
        
        # --- 2. Score Individuel ---
        texte_ton_score = self.police_petite.render("TON SCORE", True, self.GRIS_CLAIR)
        ecran.blit(texte_ton_score, (30, 95))
        
        joueur = joueurs[joueur_actuel_index]
        texte_score_perso = self.police_normale.render(str(joueur.score), True, self.BLANC)
        ecran.blit(texte_score_perso, (30, 115))

        # Ligne séparation 2
        pygame.draw.line(ecran, self.GRIS_CLAIR, (30, 140), (250, 140), 1)

        # --- 3. Quêtes (Mission) ---
        texte_mission = self.police_petite.render("MISSION (Porte de sortie)", True, self.GRIS_CLAIR)
        ecran.blit(texte_mission, (30, 145))

        # Récupération des infos depuis map_manager
        fait = map_manager.quests_completed
        total = map_manager.min_quests_to_exit
        
        # Couleur : Rouge si pas fini, Vert si fini
        couleur_quete = (255, 100, 100) if fait < total else (100, 255, 100)
        msg_quete = f"{fait} / {total} énigmes"
        
        if fait >= total:
            msg_quete = "SORTIE RÉVÉLÉE !"
        
        texte_progression = self.police_normale.render(msg_quete, True, couleur_quete)
        ecran.blit(texte_progression, (30, 160))
    
    def recompenser_enigme_reussie(self, joueur):
        joueur.gagner_points(100)
    
    def penaliser_enigme_ratee(self, joueur):
        joueur.perdre_vie()