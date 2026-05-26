import pygame

class EndScreen:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.font_titre = pygame.font.Font(None, 65)
        self.font_btn = pygame.font.Font(None, 40)
        self.btn_menu = pygame.Rect(self.largeur // 2 - 100, self.hauteur - 120, 200, 50)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_menu.collidepoint(event.pos):
                return "MENU_PRINCIPAL"
        return None

    def afficher(self, ecran, joueurs, mode_solo=False):
        ecran.fill((10, 25, 15))
        titre = self.font_titre.render("VICTOIRE !", True, (0, 255, 100))
        ecran.blit(titre, titre.get_rect(center=(self.largeur // 2, 100)))
        
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (0, 180, 80) if self.btn_menu.collidepoint(mouse_pos) else (20, 50, 30)
        pygame.draw.rect(ecran, btn_color, self.btn_menu, border_radius=8)
        pygame.draw.rect(ecran, (0, 255, 100), self.btn_menu, 2, border_radius=8)
        
        txt_btn = self.font_btn.render("Menu Principal", True, (255, 255, 255))
        ecran.blit(txt_btn, txt_btn.get_rect(center=self.btn_menu.center))