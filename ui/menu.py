import pygame

class LobbyMenu:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.font = pygame.font.Font(None, 32)
        self.chat_font = pygame.font.Font(None, 24)
        self.players_list = []
        self.chat_messages = []
        self.is_host = False
        self.local_player_id = None
        self.input_text = ""
        self.input_rect = pygame.Rect(50, self.height - 50, 400, 40)
        self.start_btn = pygame.Rect(self.width - 200, self.height - 100, 150, 50)
        self.change_btn = pygame.Rect(50, 100, 200, 40)

    def set_host(self, is_host): self.is_host = is_host
    def set_local_player_id(self, player_id): self.local_player_id = player_id
    def update_players(self, players): self.players_list = players
    def set_chat_messages(self, messages): self.chat_messages = messages

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text.strip():
                msg = self.input_text
                self.input_text = ""
                return "SEND_CHAT", msg
            elif event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable() and len(self.input_text) < 40: self.input_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_host and self.start_btn.collidepoint(event.pos): return "START_GAME", None
            if self.change_btn.collidepoint(event.pos): return "CHANGE_CHARACTER", None
        return None, None

    def draw(self, surface):
        surface.fill((30, 30, 40))
        surface.blit(self.font.render("LOBBY MULTIJOUEUR", True, (255, 255, 255)), (50, 20))
        if self.is_host:
            pygame.draw.rect(surface, (0, 200, 0), self.start_btn)
            surface.blit(self.font.render("START", True, (255, 255, 255)), (self.start_btn.x + 35, self.start_btn.y + 10))
        pygame.draw.rect(surface, (100, 100, 100), self.change_btn)
        surface.blit(self.chat_font.render("Changer Perso", True, (255, 255, 255)), (self.change_btn.x + 30, self.change_btn.y + 10))
        
        for i, j in enumerate(self.players_list):
            y = 200 + i * (j.size + 30)
            pygame.draw.rect(surface, j.couleur, (50, y, j.size, j.size))
            surface.blit(self.font.render(j.nom, True, (255, 255, 255)), (50 + j.size + 20, y + 10))
            
        pygame.draw.rect(surface, (20, 20, 20), (50, 300, 400, 300))
        for i, msg in enumerate(self.chat_messages[-10:]):
            surface.blit(self.chat_font.render(msg, True, (200, 200, 200)), (60, 310 + i * 25))
        pygame.draw.rect(surface, (50, 50, 50), self.input_rect)
        surface.blit(self.chat_font.render(self.input_text, True, (255, 255, 255)), (60, self.height - 40))