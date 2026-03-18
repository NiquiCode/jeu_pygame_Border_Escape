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

        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
        self.door_dice_results = []

        self.message = "Table (E) : Lancer les dés"
        self.font = pygame.font.Font(None, 32)
        self.font_big = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 24)

        self.transition_cooldown_ms = 300
        self.last_transition_time = 0

        self.interaction_cooldown_ms = 250
        self.last_interaction_time = 0

    def _get_player_rect(self, current_player_obj):
        return pygame.Rect(
            int(current_player_obj.x),
            int(current_player_obj.y),
            int(current_player_obj.width),
            int(current_player_obj.height)
        )

    def _interaction_pressed(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e] and now - self.last_interaction_time >= self.interaction_cooldown_ms:
            self.last_interaction_time = now
            return True

        return False

    def _player_is_on_table(self, player_rect):
        return player_rect.colliderect(self.table_rect)

    def update_message(self):
        if not self.dice_rolled:
            self.message = "Table (E) : Lancer les dés"
        else:
            self.message = f"CIBLE: {self.target_name} | JOUEURS REQUIS: {self.required_players}"

    def reset_round(self):
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
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

    def roll_dice(self, total_players_in_game):
        couleurs_portes = ["rouge", "bleu", "vert"]

        result = self.dice_manager.lancer_systeme_des(
            total_players_in_game,
            couleurs_portes
        )

        self.door_dice_results = result.get("portes", [])
        self.target_coords = result.get("salle_cible")
        self.required_players = result.get("joueurs_requis", 0)

        if self.target_coords is not None:
            self.target_name = self.map_manager.get_coordinates_str(
                self.target_coords[0],
                self.target_coords[1]
            )
        else:
            self.target_name = ""

        self.dice_rolled = self.target_coords is not None
        self.update_message()

        return result

    def apply_dice_result(self, data):
        self.door_dice_results = data.get("portes", data.get("door_dice_results", []))

        salle_cible = data.get("salle_cible", data.get("target"))
        if salle_cible is not None:
            self.target_coords = tuple(salle_cible)
        else:
            self.target_coords = None

        self.required_players = data.get("joueurs_requis", data.get("required", 0))

        if self.target_coords is not None:
            self.target_name = self.map_manager.get_coordinates_str(
                self.target_coords[0],
                self.target_coords[1]
            )
            self.dice_rolled = True
        else:
            self.target_name = ""
            self.dice_rolled = False

        self.update_message()

    def _send_dice_result_to_network(self, result):
        if not self.client:
            return

        self.client.send({
            "type": "DICE_RESULT",
            "portes": result.get("portes", []),
            "salle_cible": list(result["salle_cible"]) if result.get("salle_cible") is not None else None,
            "joueurs_requis": result.get("joueurs_requis", 0)
        })

    def _try_roll_dice(self, total_players_in_game, can_roll_dice):
        if self.dice_rolled:
            self.update_message()
            return

        if not can_roll_dice:
            self.message = "Seul l'host peut lancer les dés"
            return

        result = self.roll_dice(total_players_in_game)
        self._send_dice_result_to_network(result)

    def _handle_table_interaction(self, player_rect, total_players_in_game, can_roll_dice):
        if not self._player_is_on_table(player_rect):
            return

        if self._interaction_pressed():
            self._try_roll_dice(total_players_in_game, can_roll_dice)

    def _teleport_player_after_door(self, current_player_obj, direction):
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

    def _handle_target_room_arrival(self, current_pos, players_in_same_room):
        if not self.dice_rolled or self.target_coords is None:
            self.update_message()
            return "CENTRAL"

        if current_pos == list(self.target_coords):
            if players_in_same_room >= self.required_players:
                return "LANCER_ENIGME"

            self.message = (
                f"En attente... "
                f"({players_in_same_room}/{self.required_players} joueurs)"
            )
            return "CENTRAL"

        self.update_message()
        return "CENTRAL"

    def _handle_doors(self, current_player_obj):
        available_doors = self.check_doors_availability()
        current_time = pygame.time.get_ticks()
        player_rect = self._get_player_rect(current_player_obj)

        for direction, rect in self.doors.items():
            if direction not in available_doors:
                continue

            if not player_rect.colliderect(rect):
                continue

            if current_time - self.last_transition_time < self.transition_cooldown_ms:
                return "CENTRAL"

            current_player_obj.perdre_vie()
            moved = self.map_manager.move_player(direction)

            if not moved:
                return "CENTRAL"

            self.last_transition_time = current_time
            self._teleport_player_after_door(current_player_obj, direction)

            current_pos = self.map_manager.player_pos

            if current_pos == self.map_manager.exit_pos and self.map_manager.exit_revealed:
                return "FIN_DU_JEU"

            return "CENTRAL"

        return "CENTRAL"

    def update(self, current_player_obj, total_players_in_game=1, can_roll_dice=True):
        player_rect = self._get_player_rect(current_player_obj)

        self._handle_table_interaction(
            player_rect,
            total_players_in_game,
            can_roll_dice
        )

        door_result = self._handle_doors(current_player_obj)
        if door_result == "FIN_DU_JEU":
            return "FIN_DU_JEU"

        current_pos = self.map_manager.player_pos
        target_result = self._handle_target_room_arrival(current_pos, total_players_in_game)
        if target_result == "LANCER_ENIGME":
            return "LANCER_ENIGME"

        return "CENTRAL"

    def draw(self, screen):
        room_color = self.map_manager.get_current_room_color()
        bg_color = (
            max(0, room_color[0] // 2),
            max(0, room_color[1] // 2),
            max(0, room_color[2] // 2)
        )
        screen.fill(bg_color)

        tile_size = 50
        for x in range(0, self.width, tile_size):
            for y in range(0, self.height, tile_size):
                rect = pygame.Rect(x, y, tile_size, tile_size)

                if (x // tile_size + y // tile_size) % 2 == 0:
                    color = (
                        min(255, bg_color[0] + 18),
                        min(255, bg_color[1] + 18),
                        min(255, bg_color[2] + 18)
                    )
                else:
                    color = bg_color

                pygame.draw.rect(screen, color, rect)

        available = self.check_doors_availability()
        for direction in available:
            pygame.draw.rect(screen, (50, 50, 50), self.doors[direction])

        pygame.draw.rect(screen, (100, 60, 20), self.table_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.table_rect, 2)

        text = self.font.render(self.message, True, (255, 255, 255))
        screen.blit(
            text,
            (self.width // 2 - text.get_width() // 2, self.height // 2 - 80)
        )

        coord_txt = self.map_manager.get_coordinates_str(
            self.map_manager.player_pos[0],
            self.map_manager.player_pos[1]
        )
        lbl = self.font_big.render(coord_txt, True, (255, 255, 255))
        lbl.set_alpha(100)
        screen.blit(lbl, (50, 50))

        if self.dice_rolled and self.door_dice_results:
            y = self.height - 110
            x = 40

            for resultat in self.door_dice_results:
                couleur = resultat.get("couleur", "?")
                resultat_de = resultat.get("resultat_de", "?")
                capacite = resultat.get("capacite", "?")

                txt = self.font_small.render(
                    f"{couleur} : dé={resultat_de} | cap={capacite}",
                    True,
                    (255, 255, 255)
                )
                screen.blit(txt, (x, y))
                y += 24