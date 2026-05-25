import pygame

class ScoringSystem: 
    def __init__(self):
        self.police_titre = pygame.font.Font(None, 32)
        self.police_normale = pygame.font.Font(None, 24)
        self.police_petite = pygame.font.Font(None, 18)
        
        self.JAUNE = (255, 215, 0)
        self.BLANC = (255, 255, 255)
        self.GRIS_CLAIR = (160, 160, 180)
        self.FONCE = (20, 25, 35)
    
    def calculer_score_equipe(self, joueurs): 
        return sum(joueur.score for joueur in joueurs)
    
    def afficher_hud_score(self, ecran, joueurs, joueur_actuel_index, map_manager):
        # Positionnement structuré en haut à gauche
        x, y = 20, 20
        largeur, hauteur = 240, 150
        
        # Panneau arrière-plan épuré
        fond = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        fond.fill((20, 25, 35, 220))
        ecran.blit(fond, (x, y))
        pygame.draw.rect(ecran, self.GRIS_CLAIR, (x, y, largeur, hauteur), 1, border_radius=6)
        
        # 1. Section Équipe
        lbl_equipe = self.police_petite.render("SCORE GLOBAL", True, self.GRIS_CLAIR)
        ecran.blit(lbl_equipe, (x + 15, y + 12))
        
        score_equipe = self.calculer_score_equipe(joueurs)
        txt_score_eq = self.police_titre.render(str(score_equipe), True, self.JAUNE)
        ecran.blit(txt_score_eq, (x + 15, y + 28))
        
        # 2. Section Individuelle
        lbl_perso = self.police_petite.render("VOTRE SCORE", True, self.GRIS_CLAIR)
        ecran.blit(lbl_perso, (x + 15, y + 65))
        
        joueur = joueurs[joueur_actuel_index]
        txt_score_pe = self.police_normale.render(str(joueur.score), True, self.BLANC)
        ecran.blit(txt_score_pe, (x + 15, y + 80))
        
        # 3. Section Objectifs / Progression
        pygame.draw.line(ecran, (50, 60, 80), (x + 15, y + 110), (x + largeur - 15, y + 110), 1)
        
        fait = map_manager.quests_completed
        total = map_manager.min_quests_to_exit
        
        if fait >= total:
            msg = "SORTIE ACCESSIBLE !"
            couleur = (46, 204, 113)
        else:
            msg = f"Progression : {fait} / {total} Defis"
            couleur = (231, 76, 60)
            
        txt_prog = self.police_normale.render(msg, True, couleur)
        ecran.blit(txt_prog, (x + 15, y + 120))
    
    def recompenser_enigme_reussie(self, joueur):
        joueur.gagner_points(100)
    
    def penaliser_enigme_ratee(self, joueur):
        joueur.perdre_vie()