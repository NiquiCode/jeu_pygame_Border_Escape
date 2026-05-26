import pygame
import sys


class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_btn = pygame.font.Font(None, 45)

        btn_w, btn_h = 300, 65
        center_x = width // 2 - btn_w // 2

        self.btn_jouer = pygame.Rect(center_x, height // 2 + 30, btn_w, btn_h)
        self.btn_options = pygame.Rect(center_x, height // 2 + 110, btn_w, btn_h)
        self.btn_quitter = pygame.Rect(center_x, height // 2 + 190, btn_w, btn_h)

        try:
            self.bg = pygame.image.load("assets/menu_bg.png").convert()
            self.bg = pygame.transform.scale(self.bg, (width, height))
        except FileNotFoundError:
            self.bg = pygame.Surface((width, height))
            self.bg.fill((15, 20, 35))

    def afficher(self, ecran, horloge):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_jouer.collidepoint(event.pos):
                        return "JOUER"
                    if self.btn_options.collidepoint(event.pos):
                        return "OPTIONS"
                    if self.btn_quitter.collidepoint(event.pos):
                        return "QUITTER"

            ecran.blit(self.bg, (0, 0))
            self.dessiner_bouton(ecran, self.btn_jouer, "JOUER")
            self.dessiner_bouton(ecran, self.btn_options, "OPTIONS")
            self.dessiner_bouton(ecran, self.btn_quitter, "QUITTER")

            pygame.display.flip()
            horloge.tick(60)

    def dessiner_bouton(self, ecran, rect, texte):
        mouse_pos = pygame.mouse.get_pos()
        couleur = (0, 150, 200) if rect.collidepoint(mouse_pos) else (20, 30, 50)
        pygame.draw.rect(ecran, couleur, rect, border_radius=8)
        pygame.draw.rect(ecran, (0, 255, 255), rect, 2, border_radius=8)
        txt_surf = self.font_btn.render(texte, True, (255, 255, 255))
        ecran.blit(txt_surf, txt_surf.get_rect(center=rect.center))