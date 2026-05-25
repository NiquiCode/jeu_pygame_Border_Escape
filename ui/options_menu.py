import pygame
import sys

class OptionsMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_titre = pygame.font.Font(None, 70)
        self.font_texte = pygame.font.Font(None, 40)
        self.font_btn = pygame.font.Font(None, 45)

        self.btn_retour = pygame.Rect(width // 2 - 150, height - 100, 300, 60)
        
        # Gestion du Volume (0.0 à 1.0)
        self.volume = 0.5 
        self.btn_vol_moins = pygame.Rect(width // 2 + 60, 200, 50, 50)
        self.btn_vol_plus = pygame.Rect(width // 2 + 200, 200, 50, 50)

    def afficher(self, ecran, horloge):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_retour.collidepoint(event.pos):
                        return # Quitte les options
                    if self.btn_vol_moins.collidepoint(event.pos):
                        self.volume = max(0.0, self.volume - 0.1)
                        pygame.mixer.music.set_volume(self.volume)
                    if self.btn_vol_plus.collidepoint(event.pos):
                        self.volume = min(1.0, self.volume + 0.1)
                        pygame.mixer.music.set_volume(self.volume)

            ecran.fill((10, 15, 25))

            titre = self.font_titre.render("PARAMÈTRES", True, (0, 255, 255))
            ecran.blit(titre, titre.get_rect(center=(self.width // 2, 80)))

            # --- AUDIO ---
            txt_vol = self.font_texte.render("Volume Musique :", True, (200, 200, 200))
            ecran.blit(txt_vol, (self.width // 2 - 250, 210))

            self.dessiner_bouton(ecran, self.btn_vol_moins, "-")
            val_vol = self.font_texte.render(f"{int(self.volume * 100)}%", True, (0, 255, 150))
            ecran.blit(val_vol, val_vol.get_rect(center=(self.width // 2 + 155, 225)))
            self.dessiner_bouton(ecran, self.btn_vol_plus, "+")

            # --- CONTRÔLES ---
            pygame.draw.line(ecran, (50, 60, 80), (100, 300), (self.width - 100, 300), 2)
            
            txt_touches = self.font_titre.render("CONTRÔLES", True, (0, 255, 255))
            ecran.blit(txt_touches, txt_touches.get_rect(center=(self.width // 2, 360)))

            controles = [
                "Déplacement :  Z / Q / S / D   ou   Flèches",
                "Action / Parler :  E",
                "Carte (Minimap) :  M",
                "Quitter / Abandonner :  ESC"
            ]

            y = 430
            for c in controles:
                txt_c = self.font_texte.render(c, True, (200, 200, 200))
                ecran.blit(txt_c, txt_c.get_rect(center=(self.width // 2, y)))
                y += 45

            # --- RETOUR ---
            self.dessiner_bouton(ecran, self.btn_retour, "RETOUR")

            pygame.display.flip()
            horloge.tick(60)

    def dessiner_bouton(self, ecran, rect, texte):
        mouse_pos = pygame.mouse.get_pos()
        couleur = (0, 150, 200) if rect.collidepoint(mouse_pos) else (20, 30, 50)
        
        pygame.draw.rect(ecran, couleur, rect, border_radius=8)
        pygame.draw.rect(ecran, (0, 255, 255), rect, 2, border_radius=8)
        
        txt_surf = self.font_btn.render(texte, True, (255, 255, 255))
        ecran.blit(txt_surf, txt_surf.get_rect(center=rect.center))