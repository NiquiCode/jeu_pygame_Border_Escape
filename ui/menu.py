import pygame
from ui.character_renderer import draw_adventurer


class LobbyMenu:
    def __init__(self, largeur, hauteur, max_players=4):
        self.largeur = largeur
        self.hauteur = hauteur
        self.max_players = max_players

        self.players = []
        self.chat_messages = []

        self.is_host = False
        self.local_player_id = None
        self.min_players_to_start = 2

        self.font_title = pygame.font.SysFont("arial", 54, True)
        self.font_text = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_chat = pygame.font.SysFont("arial", 20)
        self.font_name = pygame.font.SysFont("arial", 22, True)
        self.font_info = pygame.font.SysFont("arial", 18)

        self.chat_input = ""
        self.chat_active = False

        self.room_rect = pygame.Rect(40, 130, self.largeur - 380, self.hauteur - 210)
        self.chat_rect = pygame.Rect(self.largeur - 320, 150, 250, 330)
        self.chat_input_rect = pygame.Rect(self.largeur - 320, 495, 250, 40)

    def set_host(self, is_host):
        self.is_host = is_host

    def set_local_player_id(self, player_id):
        self.local_player_id = player_id

    def set_chat_messages(self, messages):
        self.chat_messages = messages[-12:]

    def update_players(self, players):
        self.players = players[:]

    def get_local_player(self):
        for player in self.players:
            if player.player_id == self.local_player_id:
                return player
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.chat_active:
                if event.key == pygame.K_RETURN:
                    message = self.chat_input.strip()
                    self.chat_input = ""
                    self.chat_active = False
                    if message:
                        return "SEND_CHAT", message
                    return None, None

                if event.key == pygame.K_ESCAPE:
                    self.chat_active = False
                    self.chat_input = ""
                    return None, None

                if event.key == pygame.K_BACKSPACE:
                    self.chat_input = self.chat_input[:-1]
                    return None, None

                if event.unicode.isprintable() and len(self.chat_input) < 60:
                    self.chat_input += event.unicode
                    return None, None

            else:
                if event.key == pygame.K_t:
                    self.chat_active = True
                    return None, None

                if event.key == pygame.K_g and self.is_host and len(self.players) >= self.min_players_to_start:
                    return "START_GAME", None

        return None, None

    def update(self):
        joueur = self.get_local_player()
        if joueur is None or self.chat_active:
            return

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx -= joueur.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += joueur.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            dy -= joueur.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += joueur.speed

        min_x = self.room_rect.left + 10
        max_x = self.room_rect.right - 10
        min_y = self.room_rect.top + 10
        max_y = self.room_rect.bottom - 10

        joueur.move(dx, dy, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)

    def draw_background(self, surface):
        surface.fill((12, 18, 30))
        pygame.draw.rect(surface, (23, 32, 48), (0, 0, self.largeur, 90))
        pygame.draw.rect(surface, (18, 24, 36), (0, self.hauteur - 80, self.largeur, 80))

    def draw_title(self, surface):
        titre = self.font_title.render("Lobby d'attente", True, (255, 255, 255))
        surface.blit(titre, titre.get_rect(center=(self.largeur // 2, 45)))

    def draw_player_count(self, surface):
        texte = self.font_text.render(
            f"Joueurs connectés : {len(self.players)} / {self.max_players}",
            True,
            (255, 255, 255)
        )
        surface.blit(texte, (55, 100))

    def draw_room(self, surface):
        pygame.draw.rect(surface, (38, 48, 68), self.room_rect, border_radius=18)
        pygame.draw.rect(surface, (255, 255, 255), self.room_rect, 2, border_radius=18)

        center_x = self.room_rect.centerx
        base_y = self.room_rect.bottom - 130

        door_colors = [(150, 60, 60), (70, 110, 200), (70, 160, 110)]
        door_positions = [center_x - 230, center_x - 75, center_x + 80]

        for i, x in enumerate(door_positions):
            door_rect = pygame.Rect(x, base_y, 120, 110)
            pygame.draw.rect(surface, door_colors[i], door_rect, border_radius=12)
            pygame.draw.rect(surface, (255, 255, 255), door_rect, 2, border_radius=12)

    def draw_players(self, surface):
        for joueur in self.players:
            draw_adventurer(
                surface=surface,
                x=joueur.x,
                y=joueur.y,
                width=joueur.width,
                height=joueur.height,
                color=joueur.couleur,
                facing_right=joueur.facing_right,
                actif=(joueur.player_id == self.local_player_id)
            )

            nom = joueur.nom
            if getattr(joueur, "is_host", False):
                nom += " [HOST]"

            texte_nom = self.font_name.render(nom, True, (255, 255, 255))
            surface.blit(
                texte_nom,
                texte_nom.get_rect(center=(joueur.x + joueur.width // 2, joueur.y - 18))
            )

            texte_vies = self.font_info.render(f"Vies: {joueur.vies}", True, (235, 235, 235))
            surface.blit(
                texte_vies,
                texte_vies.get_rect(center=(joueur.x + joueur.width // 2, joueur.y + joueur.height + 12))
            )

    def draw_chat(self, surface):
        pygame.draw.rect(surface, (22, 28, 40), self.chat_rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), self.chat_rect, 2, border_radius=12)

        titre = self.font_text.render("Chat", True, (255, 255, 255))
        surface.blit(titre, (self.chat_rect.x + 12, self.chat_rect.y + 10))

        y = self.chat_rect.y + 45
        for msg in self.chat_messages[-12:]:
            rendu = self.font_chat.render(msg[:28], True, (220, 220, 220))
            surface.blit(rendu, (self.chat_rect.x + 10, y))
            y += 24

        pygame.draw.rect(surface, (30, 38, 55), self.chat_input_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.chat_input_rect, 2, border_radius=8)

        if self.chat_active:
            texte = self.chat_input if self.chat_input else ""
            prefix = "> "
            couleur = (255, 255, 255)
        else:
            texte = "Appuie sur T pour écrire"
            prefix = ""
            couleur = (180, 180, 180)

        rendu_input = self.font_chat.render((prefix + texte)[:26], True, couleur)
        surface.blit(rendu_input, (self.chat_input_rect.x + 10, self.chat_input_rect.y + 9))

    def draw_instructions(self, surface):
        lignes = [
            "Déplacement : ZQSD / flèches",
            "Chat : T",
        ]

        if self.is_host:
            if len(self.players) >= self.min_players_to_start:
                lignes.append("Lancer la partie : G")
            else:
                lignes.append(f"Le host peut lancer à partir de {self.min_players_to_start} joueurs")
        else:
            lignes.append("En attente du host...")

        x = 55
        y = self.hauteur - 65

        for ligne in lignes:
            rendu = self.font_small.render(ligne, True, (230, 230, 230))
            surface.blit(rendu, (x, y))
            y += 20

    def draw(self, surface):
        self.draw_background(surface)
        self.draw_title(surface)
        self.draw_player_count(surface)
        self.draw_room(surface)
        self.draw_players(surface)
        self.draw_chat(surface)
        self.draw_instructions(surface)