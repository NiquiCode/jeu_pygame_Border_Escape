import pygame

class HUD:
    def __init__(self, largeur_ecran, hauteur_ecran=700):
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.police_normale = pygame.font.Font(None, 26)
        self.police_petite = pygame.font.Font(None, 20)
        
        self.BLANC = (255, 255, 255)
        self.JAUNE = (255, 215, 0)
        self.GRIS = (25, 25, 35)
        self.GRIS_CLAIR = (120, 120, 140)
        self.ROUGE = (231, 76, 60)
        
        # 🎯 Déplacé de manière sécurisée en bas à droite
        self.btn_indice = pygame.Rect(self.largeur_ecran - 150, self.hauteur_ecran - 60, 130, 40)

    def draw_btn_indice(self, ecran, indices_restants=3):
        mx, my = pygame.mouse.get_pos()
        survol = self.btn_indice.collidepoint(mx, my)
        couleur_fond = (40, 50, 65) if survol else (30, 35, 45)
        
        pygame.draw.rect(ecran, couleur_fond, self.btn_indice, border_radius=6)
        pygame.draw.rect(ecran, self.JAUNE if survol else self.GRIS_CLAIR, self.btn_indice, 1, border_radius=6)
        
        texte = self.police_normale.render(f"Indice ({indices_restants})", True, self.BLANC)
        ecran.blit(texte, texte.get_rect(center=self.btn_indice.center))

    def afficher_liste_joueurs(self, ecran, joueurs, joueur_actuel_index):
        x = self.largeur_ecran - 270
        y = 20
        
        texte_titre = self.police_normale.render("SURVIVANTS", True, self.BLANC)
        ecran.blit(texte_titre, (x, y))
        y += 35
        
        for i, joueur in enumerate(joueurs):
            fond = pygame.Surface((250, 60), pygame.SRCALPHA)
            fond.fill((30, 35, 45, 220)) 
            ecran.blit(fond, (x, y))
            
            couleur_bordure = self.JAUNE if i == joueur_actuel_index else self.GRIS_CLAIR
            epaisseur = 2 if i == joueur_actuel_index else 1
            pygame.draw.rect(ecran, couleur_bordure, (x, y, 250, 60), epaisseur, border_radius=4)
            
            texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
            ecran.blit(texte_nom, (x + 15, y + 8))
            
            texte_score = self.police_petite.render(f"Score: {joueur.score}", True, self.JAUNE)
            ecran.blit(texte_score, (x + 15, y + 32))
            
            y += 70