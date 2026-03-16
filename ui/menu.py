import pygame
from player.lives_manager import LivesManager

pygame.init()

WIDTH, HEIGHT = 1280, 720

TITLE_FONT = pygame.font.SysFont("arial", 80, True)
INFO_FONT = pygame.font.SysFont("arial", 34, True)
NAME_FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 20)


class Player:
    def __init__(self, player_id, nom, x, y, color, is_local=False):
        self.player_id = player_id
        self.nom = nom
        self.x = x
        self.y = y
        self.width = 42
        self.height = 56
        self.color = color
        self.speed = 5
        self.vies = 0
        self.is_local = is_local

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move_keyboard(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.clamp_to_room()

    def move_mouse(self):
        mx, my = pygame.mouse.get_pos()

        target_x = mx - self.width // 2
        target_y = my - self.height // 2

        self.x += (target_x - self.x) * 0.18
        self.y += (target_y - self.y) * 0.18

        self.clamp_to_room()

    def clamp_to_room(self):
        self.x = max(40, min(self.x, WIDTH - self.width - 40))
        self.y = max(220, min(self.y, HEIGHT - self.height - 40))


class LobbyMenu:
    def __init__(self, max_players=4):
        self.max_players = max_players
        self.players = []
        self.lives_manager = LivesManager(max_vies=10)
        self.local_player_id = None
        self.use_mouse_movement = True

    # --------------------------------------------------
    # JOUEURS / CONNEXION
    # --------------------------------------------------
    def ajouter_joueur(self, player_id, nom, x, y, color, is_local=False):
        joueur = self.get_player(player_id)
        if joueur is not None:
            return joueur

        joueur = Player(player_id, nom, x, y, color, is_local=is_local)
        self.lives_manager.initialiser_vies(joueur)
        self.players.append(joueur)

        if is_local:
            self.local_player_id = player_id

        return joueur

    def supprimer_joueur(self, player_id):
        self.players = [j for j in self.players if j.player_id != player_id]

        if self.local_player_id == player_id:
            self.local_player_id = None

    def get_player(self, player_id):
        for joueur in self.players:
            if joueur.player_id == player_id:
                return joueur
        return None

    def get_local_player(self):
        if self.local_player_id is None:
            return None
        return self.get_player(self.local_player_id)

    def on_player_join(self, player_id, nom, x, y, color, is_local=False):
        return self.ajouter_joueur(player_id, nom, x, y, color, is_local=is_local)

    def on_player_leave(self, player_id):
        self.supprimer_joueur(player_id)

    def on_player_move(self, player_id, x, y):
        joueur = self.get_player(player_id)
        if joueur:
            joueur.x = x
            joueur.y = y

    def on_player_lives_update(self, player_id, vies):
        joueur = self.get_player(player_id)
        if joueur:
            joueur.vies = max(0, min(vies, self.lives_manager.max_vies))

    def sync_from_server(self, lobby_state):
        """
        Format attendu :
        {
            "max_players": 4,
            "players": [
                {
                    "id": 1,
                    "nom": "Rebecca",
                    "x": 500,
                    "y": 540,
                    "color": (255, 0, 0),
                    "vies": 10,
                    "is_local": True
                }
            ]
        }
        """
        self.max_players = lobby_state["max_players"]
        ids_recus = set()

        for pdata in lobby_state["players"]:
            pid = pdata["id"]
            ids_recus.add(pid)

            joueur = self.get_player(pid)

            if joueur is None:
                joueur = self.ajouter_joueur(
                    player_id=pid,
                    nom=pdata["nom"],
                    x=pdata["x"],
                    y=pdata["y"],
                    color=tuple(pdata["color"]),
                    is_local=pdata.get("is_local", False)
                )
            else:
                joueur.nom = pdata["nom"]
                joueur.x = pdata["x"]
                joueur.y = pdata["y"]
                joueur.color = tuple(pdata["color"])
                joueur.is_local = pdata.get("is_local", joueur.is_local)

            if "vies" in pdata:
                joueur.vies = max(0, min(pdata["vies"], self.lives_manager.max_vies))

            if joueur.is_local:
                self.local_player_id = joueur.player_id

        self.players = [j for j in self.players if j.player_id in ids_recus]

    # --------------------------------------------------
    # DEPLACEMENT
    # --------------------------------------------------
    def update_local_player_movement(self):
        joueur = self.get_local_player()
        if joueur is None:
            return

        if self.use_mouse_movement:
            joueur.move_mouse()
        else:
            keys = pygame.key.get_pressed()
            joueur.move_keyboard(keys)

    # --------------------------------------------------
    # AFFICHAGE
    # --------------------------------------------------
    def draw_background(self, surface):
        surface.fill((8, 10, 15))
        pygame.draw.circle(surface, (28, 28, 34), (WIDTH // 2, 390), 520)
        pygame.draw.rect(surface, (50, 50, 60), (WIDTH // 2 - 240, 70, 480, 12), border_radius=6)
        pygame.draw.rect(surface, (18, 18, 24), (0, 600, WIDTH, 120))

    def draw_title(self, surface):
        title = TITLE_FONT.render("LOBBY", True, (255, 255, 255))
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 85))

    def draw_player_count(self, surface):
        text = INFO_FONT.render(f"{len(self.players)} / {self.max_players} joueurs", True, (255, 255, 255))
        surface.blit(text, (30, 25))

    def draw_waiting_text(self, surface):
        if len(self.players) < self.max_players:
            msg = SMALL_FONT.render("En attente d'autres joueurs...", True, (200, 200, 200))
        else:
            msg = SMALL_FONT.render("Tous les joueurs sont connectés", True, (200, 255, 200))
        surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 180))

    def draw_doors(self, surface):
        door_width = 180
        door_height = 300

        positions = [
            WIDTH // 2 - 360,
            WIDTH // 2 - door_width // 2,
            WIDTH // 2 + 180
        ]

        colors = [
            (180, 50, 50),
            (50, 100, 220),
            (50, 180, 100)
        ]

        for i in range(3):
            x = positions[i]

            shadow = pygame.Rect(x + 8, 248, door_width, door_height)
            pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=12)

            door = pygame.Rect(x, 240, door_width, door_height)
            pygame.draw.rect(surface, colors[i], door, border_radius=12)
            pygame.draw.rect(surface, (255, 255, 255), door, 3, border_radius=12)

    def draw_room_bounds(self, surface):
        zone = pygame.Rect(30, 150, WIDTH - 60, HEIGHT - 180)
        pygame.draw.rect(surface, (255, 255, 255), zone, 2, border_radius=18)

    def draw_player(self, surface, joueur):
        pygame.draw.ellipse(
            surface,
            (0, 0, 0),
            (joueur.x - 2, joueur.y + joueur.height - 6, joueur.width + 8, 16)
        )

        shadow = pygame.Rect(joueur.x + 6, joueur.y + 6, joueur.width, joueur.height)
        pygame.draw.rect(surface, (25, 25, 25), shadow, border_radius=12)

        pygame.draw.rect(surface, joueur.color, joueur.rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), joueur.rect, 2, border_radius=12)

        visor = pygame.Rect(joueur.x + 8, joueur.y + 12, 26, 14)
        pygame.draw.rect(surface, (180, 235, 255), visor, border_radius=7)
        pygame.draw.rect(surface, (40, 40, 40), visor, 2, border_radius=7)

    def draw_name(self, surface, joueur):
        text = NAME_FONT.render(joueur.nom, True, (255, 255, 255))
        surface.blit(
            text,
            (joueur.x + joueur.width // 2 - text.get_width() // 2, joueur.y - 54)
        )

    def draw_life_dots(self, surface, joueur):
        vies_affichees = max(0, min(joueur.vies, self.lives_manager.max_vies))

        if vies_affichees <= 0:
            return

        dot_radius = 4
        spacing = 12
        total_width = (vies_affichees - 1) * spacing
        start_x = joueur.x + joueur.width // 2 - total_width // 2
        y = joueur.y - 24

        for i in range(vies_affichees):
            cx = start_x + i * spacing
            pygame.draw.circle(surface, (220, 40, 40), (cx, y), dot_radius)
            pygame.draw.circle(surface, (255, 255, 255), (cx, y), dot_radius, 1)

    def draw_lobby(self, surface):
        self.draw_background(surface)
        self.draw_title(surface)
        self.draw_player_count(surface)
        self.draw_waiting_text(surface)
        self.draw_doors(surface)
        self.draw_room_bounds(surface)

        for joueur in self.players:
            self.draw_player(surface, joueur)
            self.draw_name(surface, joueur)
            self.draw_life_dots(surface, joueur)

    # --------------------------------------------------
    # LIEN AVEC LIVES MANAGER
    # --------------------------------------------------
    def joueur_reste_meme_salle(self, player_id):
        joueur = self.get_player(player_id)
        if joueur:
            self.lives_manager.perte_rester_meme_salle(joueur)

    def joueur_premier_entree_salle(self, player_id):
        joueur = self.get_player(player_id)
        if joueur:
            self.lives_manager.perte_entree_salle(joueur)

    def joueur_perd_vie(self, player_id, nb=1):
        joueur = self.get_player(player_id)
        if joueur:
            self.lives_manager.perdre_vie(joueur, nb)

    def joueur_ajoute_vie(self, player_id, nb=1):
        joueur = self.get_player(player_id)
        if joueur:
            self.lives_manager.ajouter_vie(joueur, nb)

    def reset_joueur(self, player_id):
        joueur = self.get_player(player_id)
        if joueur:
            self.lives_manager.reset_joueur(joueur)

    def appliquer_blocage_depuis_salles(self, index_salle, salles):
        self.lives_manager.appliquer_blocage_solitude(index_salle, salles)


# --------------------------------------------------
# DEMO LOCALE POUR TEST
# A supprimer plus tard si tu branches le vrai réseau
# --------------------------------------------------
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lobby d'attente")
    clock = pygame.time.Clock()

    lobby = LobbyMenu(max_players=4)

    local_player = lobby.on_player_join(
        player_id=1,
        nom="Rebecca",
        x=560,
        y=520,
        color=(230, 190, 60),
        is_local=True
    )

    lobby.on_player_join(2, "A", 420, 540, (200, 70, 70))
    lobby.on_player_join(3, "B", 680, 520, (70, 120, 230))
    lobby.on_player_join(4, "C", 880, 540, (70, 200, 120))

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    lobby.use_mouse_movement = not lobby.use_mouse_movement
                elif event.key == pygame.K_1:
                    lobby.joueur_premier_entree_salle(1)
                elif event.key == pygame.K_2:
                    lobby.joueur_reste_meme_salle(1)
                elif event.key == pygame.K_3:
                    lobby.joueur_perd_vie(1, 1)
                elif event.key == pygame.K_r:
                    lobby.reset_joueur(1)

        lobby.update_local_player_movement()
        lobby.draw_lobby(screen)
        pygame.display.flip()

    pygame.quit()
