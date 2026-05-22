import pygame

class DeathScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_big = pygame.font.Font(None, 80)
        self.font_btn = pygame.font.Font(None, 40)
        
        # Bouton Rejouer
        self.btn_rejouer_rect = pygame.Rect(0, 0, 250, 60)
        self.btn_rejouer_rect.center = (width // 2, height // 2 + 50)
        
        # Bouton Retour Lobby
        self.btn_lobby_rect = pygame.Rect(0, 0, 250, 60)
        self.btn_lobby_rect.center = (width // 2, height // 2 + 130)

    def handle_input(self, event):
        """
        Retourne :
        - "REJOUER" si le joueur clique sur Rejouer
        - "LOBBY" si le joueur clique sur Retour Lobby
        - None sinon
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if self.btn_rejouer_rect.collidepoint(event.pos):
                    return "REJOUER"
                elif self.btn_lobby_rect.collidepoint(event.pos):
                    return "LOBBY"
        return None

    def draw(self, screen):
        # Fond rouge sang semi-transparent
        surf = pygame.Surface((self.width, self.height))
        surf.fill((50, 0, 0))
        surf.set_alpha(200)
        screen.blit(surf, (0,0))
        
        # Texte MORT
        txt = self.font_big.render("VOUS ÊTES MORT", True, (255, 0, 0))
        rect = txt.get_rect(center=(self.width//2, self.height//2 - 50))
        screen.blit(txt, rect)
        
        # --- Dessin Bouton Rejouer ---
        pygame.draw.rect(screen, (200, 200, 200), self.btn_rejouer_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.btn_rejouer_rect, 3)
        lbl_r = self.font_btn.render("REJOUER", True, (0, 0, 0))
        screen.blit(lbl_r, lbl_r.get_rect(center=self.btn_rejouer_rect.center))

        # --- Dessin Bouton Retour Lobby ---
        pygame.draw.rect(screen, (100, 150, 200), self.btn_lobby_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.btn_lobby_rect, 3)
        lbl_l = self.font_btn.render("RETOUR LOBBY", True, (0, 0, 0))
        screen.blit(lbl_l, lbl_l.get_rect(center=self.btn_lobby_rect.center))