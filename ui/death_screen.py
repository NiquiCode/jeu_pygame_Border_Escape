#écran de mort quand un joueur meurt
import pygame

class DeathScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_big = pygame.font.Font(None, 80)
        self.font_btn = pygame.font.Font(None, 40)
        
        # Bouton Rejouer
        self.btn_rect = pygame.Rect(0, 0, 200, 60)
        self.btn_rect.center = (width // 2, height // 2 + 100)

    def handle_input(self, event):
        """Retourne True si le joueur clique sur Rejouer"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if self.btn_rect.collidepoint(event.pos):
                    return True
        return False

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
        
        # Bouton Rejouer
        pygame.draw.rect(screen, (200, 200, 200), self.btn_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.btn_rect, 3)
        
        lbl = self.font_btn.render("REJOUER", True, (0, 0, 0))
        lbl_rect = lbl.get_rect(center=self.btn_rect.center)
        screen.blit(lbl, lbl_rect)