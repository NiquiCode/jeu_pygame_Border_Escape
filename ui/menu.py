import pygame

class LobbyMenu:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.font_titre = pygame.font.Font(None, 60)
        self.font_texte = pygame.font.Font(None, 36)
        self.players = []
        self.is_host = False
        self.local_player_id = None
        self.btn_start = pygame.Rect(largeur // 2 - 100, hauteur - 100, 200, 50)

    def set_host(self, is_host):
        self.is_host = is_host

    def set_local_player_id(self, player_id):
        self.local_player_id = player_id

    def update_players(self, players_list):
        self.players = players_list

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_host and self.btn_start.collidepoint(event.pos):
                return "START_GAME", None
        return None, None

    def draw(self, screen):
        screen.fill((20, 30, 40))
        
        titre = self.font_titre.render("SALON MULTIJOUEUR", True, (0, 255, 255))
        screen.blit(titre, (self.largeur // 2 - titre.get_width() // 2, 50))

        y = 150
        for p in self.players:
            texte = f"- {p.nom}"
            if p.player_id == self.local_player_id:
                texte += " (Toi)"
            txt_surface = self.font_texte.render(texte, True, (255, 255, 255))
            screen.blit(txt_surface, (self.largeur // 2 - 150, y))
            y += 40

        if self.is_host:
            pygame.draw.rect(screen, (0, 200, 50), self.btn_start, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), self.btn_start, 2, border_radius=8)
            txt_btn = self.font_texte.render("LANCER", True, (255, 255, 255))
            screen.blit(txt_btn, txt_btn.get_rect(center=self.btn_start.center))
        else:
            txt_wait = self.font_texte.render("En attente de l'hôte...", True, (200, 200, 200))
            screen.blit(txt_wait, (self.largeur // 2 - txt_wait.get_width() // 2, self.hauteur - 80))