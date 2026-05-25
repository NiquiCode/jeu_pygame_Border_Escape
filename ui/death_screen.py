import pygame

class DeathScreen:
    def __init__(self, largeur, hauteur):
        self.largeur, self.hauteur = largeur, hauteur
        self.font_titre = pygame.font.SysFont(None, 80)
        self.font_btn = pygame.font.SysFont(None, 40)
        self.btn_rejouer = pygame.Rect(largeur//2 - 100, hauteur//2, 200, 50)
        self.btn_spectateur = pygame.Rect(largeur//2 - 120, hauteur//2 + 70, 240, 50)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_rejouer.collidepoint(event.pos): return "REJOUER"
            if self.btn_spectateur.collidepoint(event.pos): return "SPECTATEUR"
        return None

    def draw(self, screen, mode_solo=False):
        screen.fill((20, 0, 0))
        titre = self.font_titre.render("VOUS ÊTES MORT", True, (255, 0, 0))
        screen.blit(titre, (self.largeur//2 - titre.get_width()//2, self.hauteur//2 - 100))
        
        pygame.draw.rect(screen, (150, 0, 0), self.btn_rejouer)
        screen.blit(self.font_btn.render("REJOUER", True, (255, 255, 255)), (self.btn_rejouer.x + 35, self.btn_rejouer.y + 10))
        
        if not mode_solo:
            pygame.draw.rect(screen, (50, 50, 150), self.btn_spectateur)
            screen.blit(self.font_btn.render("SPECTATEUR", True, (255, 255, 255)), (self.btn_spectateur.x + 30, self.btn_spectateur.y + 10))