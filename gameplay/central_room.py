import pygame
from player.dice import DiceManager


class CentralRoom:
    def __init__(self, screen_width, screen_height, map_manager, client=None):
        self.width = screen_width
        self.height = screen_height
        self.map_manager = map_manager
        self.client = client

        self.dice_manager = DiceManager()

        self.table_rect = pygame.Rect(0, 0, 120, 100)
        self.table_rect.center = (screen_width // 2, screen_height // 2)

        mid_x, mid_y = screen_width // 2, screen_height // 2
        self.doors = {
            "HAUT": pygame.Rect(mid_x - 50, 0, 100, 20),
            "BAS": pygame.Rect(mid_x - 50, screen_height - 20, 100, 20),
            "GAUCHE": pygame.Rect(0, mid_y - 50, 20, 100),
            "DROITE": pygame.Rect(screen_width - 20, mid_y - 50, 20, 100)
        }

        # État du tour
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
        self.players_arrived_count = 0

        # Résultats des dés liés aux portes
        self.door_dice_results = []

        self.message = "Table (E) : Lancer les dés"
        self.font = pygame.font.Font(None, 32)
        self.font_big = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 24)

        # Cooldown anti-déclenchement multiple sur une porte
        self.transition_cooldown_ms = 300
        self.last_transition_time = 0

    def _get_player_rect(self, current_player_obj):
        return pygame.Rect(
            current_player_obj.x,
            current_player_obj.y,
            current_player_obj.width,
            current_player_obj.height
        )

    def roll_dice(self, total_players_in_game):
        """
        Lance les dés du tour :
        - capacité des portes
        - salle cible
        - nombre de joueurs requis
        """
        couleurs_portes = ["rouge", "bleu", "vert"]

        result = self.dice_manager.lancer_systeme_des(
            total_players_in_game,
            couleurs_portes
        )

        self.door_dice_results = result["portes"]
        self.target_coords = result["salle_cible"]
        self.required_players = result["joueurs_requis"]
        self.target_name = self.map_manager.get_coordinates_str(
            self.target_coords[0],
            self.target_coords[1]
        )

        self.dice_rolled = True
        self.players_arrived_count = 0
        self.update_message()

    def apply_dice_result(self, data):
        """
        Applique un résultat de dés reçu du réseau.
        Compatible avec un message du type :
        {
            "type": "DICE_RESULT",
            "portes": [...],
            "salle_cible": [x, y],
            "joueurs_requis": n
        }
        ou variantes target / required.
        """
        self.door_dice_results = data.get("portes", data.get("door_dice_results", []))

        salle_cible = data.get("salle_cible", data.get("target"))
        if salle_cible is not None:
            self.target_coords = tuple(salle_cible)

        self.required_players = data.get("joueurs_requis", data.get("required", 0))

        if self.target_coords is not None:
            self.target_name = self.map_manager.get_coordinates_str(
                self.target_coords[0],
                self.target_coords[1]
            )
        else:
            self.target_name = ""

        self.dice_rolled = self.target_coords is not None
        self.players_arrived_count = 0
        self.update_message()

    def update_message(self):
        if not self.dice_rolled:
            self.message = "Table (E) : Lancer les dés"
        else:
            self.message = f"CIBLE: {self.target_name} | JOUEURS REQUIS: {self.required_players}"

    def reset_round(self):
        """Appelé après une réussite d'énigme."""
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
        self.players_arrived_count = 0
        self.door_dice_results = []
        self.update_message()

    def check_doors_availability(self):
        px, py = self.map_manager.player_pos
        available = []

        if py > 0:
            available.append("HAUT")
        if py < 2:
            available.append("BAS")
        if px > 0:
            available.append("GAUCHE")
        if px < 2:
            available.append("DROITE")

        return available

    def _send_roll_dice_request(self, total_players_in_game):
        """
        Si un client réseau existe, on demande au serveur de lancer les dés.
        Sinon, on lance localement.
        """
        if self.client:
            self.client.send({
                "type": "ROLL_DICE",
                "players": total_players_in_game
            })
        else:
            self.roll_dice(total_players_in_game)

    def _send_move_request(self, current_player_obj, direction):
        """
        Si un client réseau existe, on signale le déplacement au serveur.
        Sinon, le déplacement reste local.
        """
        if self.client:
            self.client.send({
                "type": "MOVE",
                "id": current_player_obj.player_id,
                "dir": direction
            })

    def update(self, current_player_obj, total_players_in_game=1):
        """
        current_player_obj : objet Player local
        total_players_in_game : nombre total de joueurs visibles dans la partie
        """
        player_rect = self._get_player_rect(current_player_obj)
        keys = pygame.key.get_pressed()

        # --- TABLE (Lancer les dés) ---
        if player_rect.colliderect(self.table_rect):
            if keys[pygame.K_e] and not self.dice_rolled:
                self._send_roll_dice_request(total_players_in_game)

        # --- PORTES (Déplacement) ---
        available_doors = self.check_doors_availability()
        current_time = pygame.time.get_ticks()

        for direction, rect in self.doors.items():
            if direction in available_doors and player_rect.colliderect(rect):
                if current_time - self.last_transition_time < self.transition_cooldown_ms:
                    return "CENTRAL"

                current_player_obj.perdre_vie()
                print(f"-1 Vie pour déplacement. Reste: {current_player_obj.vies}")

                moved = self.map_manager.move_player(direction)

                if moved:
                    self.last_transition_time = current_time

                    self._send_move_request(current_player_obj, direction)

                    if direction == "HAUT":
                        current_player_obj.y = self.height - current_player_obj.height - 40
                    elif direction == "BAS":
                        current_player_obj.y = 40
                    elif direction == "GAUCHE":
                        current_player_obj.x = self.width - current_player_obj.width - 40
                        if hasattr(current_player_obj, "facing_right"):
                            current_player_obj.facing_right = False
                    elif direction == "DROITE":
                        current_player_obj.x = 40
                        if hasattr(current_player_obj, "facing_right"):
                            current_player_obj.facing_right = True

                    current_pos = self.map_manager.player_pos

                    if current_pos == self.map_manager.exit_pos and self.map_manager.exit_revealed:
                        return "FIN_DU_JEU"

                    if self.dice_rolled and current_pos == list(self.target_coords):
                        self.players_arrived_count += 1
                        print(
                            f"Arrivé cible ! Compteur: "
                            f"{self.players_arrived_count}/{self.required_players}"
                        )

                        if self.players_arrived_count >= self.required_players:
                            return "LANCER_ENIGME"
                        else:
                            self.message = (
                                f"En attente... "
                                f"({self.players_arrived_count}/{self.required_players} joueurs)"
                            )
                    else:
                        self.update_message()

                return "CENTRAL"

        return "CENTRAL"

    def draw(self, screen):
        room_color = self.map_manager.get_current_room_color()
        bg_color = (
            room_color[0] // 2,
            room_color[1] // 2,
            room_color[2] // 2
        )
        screen.fill(bg_color)

        # Portes
        available = self.check_doors_availability()
        for direction in available:
            pygame.draw.rect(screen, (50, 50, 50), self.doors[direction])

        # Table
        pygame.draw.rect(screen, (100, 60, 20), self.table_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.table_rect, 2)

        # Message principal
        text = self.font.render(self.message, True, (255, 255, 255))
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80))

        # Coordonnées actuelles
        coord_txt = self.map_manager.get_coordinates_str(
            self.map_manager.player_pos[0],
            self.map_manager.player_pos[1]
        )
        lbl = self.font_big.render(coord_txt, True, (255, 255, 255))
        lbl.set_alpha(100)
        screen.blit(lbl, (50, 50))

        # Affichage des résultats de dés des portes
        if self.dice_rolled and self.door_dice_results:
            y = self.height - 110
            x = 40

            for resultat in self.door_dice_results:
                txt = self.font_small.render(
                    f"{resultat['couleur']} : dé={resultat['resultat_de']} | cap={resultat['capacite']}",
                    True,
                    (255, 255, 255)
                )
                screen.blit(txt, (x, y))
                y += 24