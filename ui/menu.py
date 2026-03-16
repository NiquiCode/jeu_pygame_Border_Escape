import pygame


class LobbyMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.title_font = pygame.font.SysFont("arial", 80, True)
        self.player_font = pygame.font.SysFont("arial", 28)
        self.info_font = pygame.font.SysFont("arial", 32)
        self.chat_font = pygame.font.SysFont(None, 26)

        self.players = []
        self.chat_messages = []
        self.chat_input = ""
        self.is_host = False

    def set_host(self, is_host):
        self.is_host = is_host

    def update_players(self, players):
        self.players = players

    def update_chat_input(self, value):
        self.chat_input = value

    def set_chat_messages(self, messages):
        self.chat_messages = messages[-30:]

    def handle_event(self, event):
        """
        Retourne :
        - ("SEND_CHAT", message)
        - ("START_GAME", None)
        - (None, None)
        """
        if event.type != pygame.KEYDOWN:
            return None, None

        if event.key == pygame.K_RETURN:
            message = self.chat_input.strip()
            self.chat_input = ""
            if message:
                return "SEND_CHAT", message
            return None, None

        if self.is_host and event.key == pygame.K_SPACE:
            return "START_GAME", None

        if event.key == pygame.K_BACKSPACE:
            self.chat_input = self.chat_input[:-1]
            return None, None

        if event.unicode.isprintable() and len(self.chat_input) < 60:
            self.chat_input += event.unicode

        return None, None

    def draw_background(self, screen):
        screen.fill((8, 10, 15))
        pygame.draw.circle(screen, (30, 30, 35), (self.width // 2, 400), 520)
        pygame.draw.rect(
            screen,
            (50, 50, 60),
            (self.width // 2 - 200, 70, 400, 12),
            border_radius=6
        )

    def draw_player_count(self, screen):
        text = self.info_font.render(f"Players : {len(self.players)}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

    def draw_title(self, screen):
        title = self.title_font.render("LOBBY", True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 90))

    def draw_doors(self, screen):
        door_width = 180
        door_height = 300

        door_positions = [
            self.width // 2 - 360,
            self.width // 2 - door_width // 2,
            self.width // 2 + 180
        ]

        door_colors = [
            (180, 50, 50),
            (50, 100, 220),
            (50, 180, 100)
        ]

        for i in range(3):
            x = door_positions[i]

            shadow = pygame.Rect(x + 8, 248, door_width, door_height)
            pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=12)

            door = pygame.Rect(x, 240, door_width, door_height)
            pygame.draw.rect(screen, door_colors[i], door, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), door, 3, border_radius=12)

        return door_positions

    def draw_dice(self, screen, door_positions):
        size = 80

        dice_colors = [
            (200, 60, 60),
            (60, 120, 220),
            (60, 200, 120)
        ]

        for i in range(3):
            x = door_positions[i] + 90 - size // 2
            y = 580

            dice = pygame.Rect(x, y, size, size)

            pygame.draw.rect(screen, dice_colors[i], dice, border_radius=12)
            pygame.draw.rect(screen, (30, 30, 30), dice, 3, border_radius=12)

            dots = [
                (x + 20, y + 20),
                (x + 60, y + 20),
                (x + 20, y + 60),
                (x + 60, y + 60),
                (x + 40, y + 40)
            ]

            for dot in dots:
                pygame.draw.circle(screen, (0, 0, 0), dot, 6)

    def draw_players_list(self, screen):
        start_y = 540

        for i, player in enumerate(self.players):
            y = start_y + i * 40

            name = self.player_font.render(player.nom, True, (255, 255, 255))
            screen.blit(name, (80, y))

            vies_affichees = min(player.vies, 10)
            for v in range(vies_affichees):
                pygame.draw.circle(
                    screen,
                    (220, 40, 40),
                    (200 + v * 14, y + 14),
                    6
                )

    def draw_chat(self, screen):
        chat_box = pygame.Rect(780, 140, 450, 360)
        pygame.draw.rect(screen, (30, 38, 58), chat_box)
        pygame.draw.rect(screen, (255, 255, 255), chat_box, 2)

        chat_title = self.info_font.render("Chat", True, (255, 255, 255))
        screen.blit(chat_title, (790, 105))

        visible_messages = self.chat_messages[-10:]
        y_msg = 160
        for msg in visible_messages:
            texte = self.chat_font.render(msg, True, (235, 235, 235))
            screen.blit(texte, (795, y_msg))
            y_msg += 30

        input_box = pygame.Rect(780, 530, 450, 50)
        pygame.draw.rect(screen, (40, 55, 85), input_box)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        prefix = self.chat_font.render("> ", True, (255, 255, 255))
        input_surface = self.chat_font.render(
            self.chat_input if self.chat_input else "Écris un message...",
            True,
            (255, 255, 255) if self.chat_input else (160, 160, 160)
        )
        screen.blit(prefix, (792, 542))
        screen.blit(input_surface, (815, 542))

    def draw_footer(self, screen):
        if self.is_host:
            info = self.info_font.render("Espace : lancer la partie", True, (255, 255, 255))
        else:
            info = self.info_font.render("En attente du lancement par l'host...", True, (200, 200, 200))

        screen.blit(info, info.get_rect(center=(self.width // 2, self.height - 40)))

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_player_count(screen)
        self.draw_title(screen)

        door_positions = self.draw_doors(screen)
        self.draw_dice(screen, door_positions)
        self.draw_players_list(screen)
        self.draw_chat(screen)
        self.draw_footer(screen)