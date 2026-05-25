import pygame

class EndScreen: 
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

        # Création des boutons (placés en bas de l'écran)
        self.btn_rejouer_rect = pygame.Rect(self.largeur // 2 - 260, self.hauteur - 80, 200, 50)
        self.btn_retour_rect = pygame.Rect(self.largeur // 2 + 60, self.hauteur - 80, 200, 50)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.btn_rejouer_rect.collidepoint(event.pos):
                    return "REJOUER"
                if self.btn_retour_rect.collidepoint(event.pos):
                    return "RETOUR"
        return None

    def afficher(self, ecran, joueurs, mode_solo=False): 
        #Fond semi-transparent
        fond = pygame.Surface((self.largeur, self.hauteur))
        fond.fill(self.NOIR)
        fond.set_alpha(230)
        ecran.blit(fond, (0, 0))
        
        #Titre
        texte_titre = self.police_titre.render("🏆 MISSION TERMINÉE 🏆", True, self.JAUNE)
        rect_titre = texte_titre.get_rect(center=(self.largeur // 2, 80))
        ecran.blit(texte_titre, rect_titre)
        
        #Score collectif
        score_total = sum(j.score for j in joueurs)
        texte_label = self.police_petite.render("SCORE COLLECTIF", True, self.GRIS_CLAIR)
        rect_label = texte_label.get_rect(center=(self.largeur // 2, 130))
        ecran.blit(texte_label, rect_label)
        
        texte_score = self.police_titre.render(str(score_total), True, self.JAUNE)
        rect_score = texte_score.get_rect(center=(self.largeur // 2, 160))
        ecran.blit(texte_score, rect_score)
        
        #Trier les joueurs
        joueurs_tries = sorted(joueurs, key=lambda j: j.score, reverse=True)
        
        #Afficher classement
        y = 220
        medailles = ["🥇", "🥈", "🥉"]
        
        for i, joueur in enumerate(joueurs_tries):
            couleur_fond = (100, 80, 0) if i == 0 else self.GRIS
            fond_joueur = pygame.Surface((600, 70))
            fond_joueur.fill(couleur_fond)
            ecran.blit(fond_joueur, (self.largeur // 2 - 300, y))
            
            couleur_bordure = self.JAUNE if i == 0 else self.GRIS_CLAIR
            pygame.draw.rect(ecran, couleur_bordure, (self.largeur // 2 - 300, y, 600, 70), 3)
            
            medaille = medailles[i] if i < 3 else f"{i+1}"
            texte_rang = self.police_titre.render(medaille, True, self.BLANC)
            ecran.blit(texte_rang, (self.largeur // 2 - 280, y + 15))
            
            couleur_nom = self.JAUNE if i == 0 else self.BLANC
            texte_nom = self.police_normale.render(joueur.nom, True, couleur_nom)
            ecran.blit(texte_nom, (self.largeur // 2 - 220, y + 20))
            
            texte_score_j = self.police_normale.render(str(joueur.score), True, self.JAUNE)
            ecran.blit(texte_score_j, (self.largeur // 2 + 150, y + 20))
            
            texte_vies = self.police_petite.render(f"{joueur.vies} vies", True, self.GRIS_CLAIR)
            ecran.blit(texte_vies, (self.largeur // 2 + 50, y + 25))
            
            y += 80
        
        # --- Dessin Bouton Rejouer ---
        pygame.draw.rect(ecran, (200, 200, 200), self.btn_rejouer_rect)
        pygame.draw.rect(ecran, (0, 0, 0), self.btn_rejouer_rect, 3)
        lbl_r = self.police_normale.render("REJOUER", True, (0, 0, 0))
        ecran.blit(lbl_r, lbl_r.get_rect(center=self.btn_rejouer_rect.center))

        # --- Dessin Bouton Dynamique ---
        pygame.draw.rect(ecran, (100, 150, 200), self.btn_retour_rect)
        pygame.draw.rect(ecran, (0, 0, 0), self.btn_retour_rect, 3)
        
        texte_bouton = "MENU PRINCIPAL" if mode_solo else "RETOUR LOBBY"
        lbl_l = self.police_normale.render(texte_bouton, True, (0, 0, 0))
        ecran.blit(lbl_l, lbl_l.get_rect(center=self.btn_retour_rect.center))