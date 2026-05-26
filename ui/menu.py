import pygame
import time

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

        self.font_title = pygame.font.SysFont("impact", 58)
        self.font_subtitle = pygame.font.SysFont("consolas", 22, True)
        self.font_text = pygame.font.SysFont("consolas", 20)
        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_chat = pygame.font.SysFont("consolas", 18, True)
        self.font_name = pygame.font.SysFont("consolas", 20, True)
        self.font_info = pygame.font.SysFont("consolas", 16)

        self.chat_input = ""
        self.chat_active = False

        self.room_rect = pygame.Rect(40, 130, self.largeur - 380, self.hauteur - 210)
        
        try:
            bg_image = pygame.image.load("assets/herbe_sol_lobby.png").convert()
            self.room_bg = pygame.transform.scale(bg_image, (self.room_rect.width, self.room_rect.height))
        except FileNotFoundError:
            self.room_bg = pygame.Surface((self.room_rect.width, self.room_rect.height))
            self.room_bg.fill((20, 25, 30)) 
            
        self.dark_overlay = pygame.Surface((self.room_rect.width, self.room_rect.height))
        self.dark_overlay.set_alpha(170)
        self.dark_overlay.fill((10, 12, 18))

        self.kiosk_rect = pygame.Rect(self.room_rect.x + 50, self.room_rect.y + 50, 80, 90)
        self.chat_rect = pygame.Rect(self.largeur - 320, 130, 280, 350)
        self.chat_input_rect = pygame.Rect(self.largeur - 320, 495, 280, 40)

    def set_host(self, is_host):
        self.is_host = is_host

    def set_local_player_id(self, player_id):
        self.local_player_id = player_id

    def set_chat_messages(self, messages):
        self.chat_messages = messages[-14:]

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
                if event.key == pygame.K_e:
                    joueur = self.get_local_player()
                    if joueur and joueur.rect.colliderect(self.kiosk_rect):
                        return "CHANGE_CHARACTER", None
        return None, None

    def update(self):
        joueur = self.get_local_player()
        if joueur is None or self.chat_active:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: dx -= joueur.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += joueur.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]: dy -= joueur.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += joueur.speed

        min_x = self.room_rect.left + 15
        max_x = self.room_rect.right - 15
        min_y = self.room_rect.top + 15
        max_y = self.room_rect.bottom - 15

        joueur.move(dx, dy, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
        joueur.update()

    def draw_background(self, surface):
        surface.fill((8, 10, 14))
        pygame.draw.rect(surface, (15, 20, 25), (0, 0, self.largeur, 90))
        pygame.draw.line(surface, (0, 255, 204), (0, 90), (self.largeur, 90), 2)
        pygame.draw.rect(surface, (15, 20, 25), (0, self.hauteur - 80, self.largeur, 80))
        pygame.draw.line(surface, (255, 50, 50), (0, self.hauteur - 80), (self.largeur, self.hauteur - 80), 2)

    def draw_title(self, surface):
        titre = self.font_title.render("ZONE DE QUARANTAINE", True, (240, 240, 240))
        surface.blit(titre, titre.get_rect(center=(self.largeur // 2, 35)))
        sous_titre = self.font_subtitle.render("// CONNEXION AU SYSTEME BORDER ESCAPE //", True, (0, 200, 150))
        surface.blit(sous_titre, sous_titre.get_rect(center=(self.largeur // 2, 75)))

    def draw_player_count(self, surface):
        status_color = (0, 255, 100) if len(self.players) >= self.min_players_to_start else (255, 150, 50)
        texte = self.font_text.render(f"> SUJETS DETECTES : {len(self.players)} / {self.max_players}", True, status_color)
        surface.blit(texte, (40, 100))

    def draw_room(self, surface):
        surface.blit(self.room_bg, self.room_rect.topleft)
        surface.blit(self.dark_overlay, self.room_rect.topleft)
        pygame.draw.rect(surface, (40, 45, 50), self.room_rect, 4)
        pygame.draw.rect(surface, (0, 200, 255), self.room_rect, 1)

        pygame.draw.rect(surface, (30, 10, 10), self.kiosk_rect)
        pygame.draw.rect(surface, (200, 50, 50), self.kiosk_rect, 2)
        
        ecran_borne = pygame.Rect(self.kiosk_rect.x + 10, self.kiosk_rect.y + 15, self.kiosk_rect.width - 20, 35)
        color_screen = (0, 255, 200) if int(time.time() * 2) % 2 == 0 else (0, 150, 100)
        pygame.draw.rect(surface, color_screen, ecran_borne)
        
        txt_borne = self.font_small.render("ADN", True, (0,0,0))
        surface.blit(txt_borne, txt_borne.get_rect(center=ecran_borne.center))

        joueur = self.get_local_player()
        if joueur and joueur.rect.colliderect(self.kiosk_rect):
            prompt = self.font_text.render("[E] MODIFIER PROFIL", True, (255, 255, 100))
            bg_prompt = pygame.Rect(self.kiosk_rect.centerx - prompt.get_width()//2 - 5, self.kiosk_rect.top - 25, prompt.get_width() + 10, prompt.get_height() + 4)
            pygame.draw.rect(surface, (20, 20, 20), bg_prompt)
            pygame.draw.rect(surface, (255, 255, 100), bg_prompt, 1)
            surface.blit(prompt, (bg_prompt.x + 5, bg_prompt.y + 2))

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
            nom_original = joueur.nom
            host_tag = ""
            name_color = (255, 255, 255)
            
            if getattr(joueur, "is_host", False):
                host_tag = " [ADMIN]"
                name_color = (255, 50, 50)

            # --- CORRECTION DU DÉDOUBLEMENT ---
            # On vide temporairement le nom pour éviter que player.py l'écrive par-dessus
            joueur.nom = ""
            joueur.draw(surface, self.font_name, actif=(joueur.player_id == self.local_player_id))
            joueur.nom = nom_original
            # ----------------------------------
            
            texte_nom = self.font_name.render(joueur.nom + host_tag, True, name_color)
            surface.blit(texte_nom, texte_nom.get_rect(center=(joueur.x + joueur.size // 2, joueur.y - 18)))

            texte_vies = self.font_info.render(f"HP: {joueur.vies}", True, (150, 255, 150))
            surface.blit(texte_vies, texte_vies.get_rect(center=(joueur.x + joueur.size // 2, joueur.y + joueur.size + 8)))

    def draw_chat(self, surface):
        pygame.draw.rect(surface, (5, 5, 8), self.chat_rect)
        pygame.draw.rect(surface, (50, 255, 50), self.chat_rect, 1)

        titre = self.font_text.render(">> LOGS SYSTEME", True, (50, 255, 50))
        surface.blit(titre, (self.chat_rect.x + 10, self.chat_rect.y + 10))
        pygame.draw.line(surface, (50, 255, 50), (self.chat_rect.x, self.chat_rect.y + 35), (self.chat_rect.right, self.chat_rect.y + 35), 1)

        y = self.chat_rect.y + 45
        for msg in self.chat_messages:
            rendu = self.font_chat.render(msg[:32], True, (0, 200, 100))
            surface.blit(rendu, (self.chat_rect.x + 10, y))
            y += 20

        pygame.draw.rect(surface, (15, 15, 20), self.chat_input_rect)
        border_color = (255, 255, 255) if self.chat_active else (100, 100, 100)
        pygame.draw.rect(surface, border_color, self.chat_input_rect, 1)

        if self.chat_active:
            texte = self.chat_input if self.chat_input else ""
            cursor = "_" if int(time.time() * 2) % 2 == 0 else " "
            prefix = "C:\\> "
            rendu_input = self.font_chat.render((prefix + texte + cursor)[:32], True, (255, 255, 255))
        else:
            texte = "[T] INSERER COMMANDE"
            rendu_input = self.font_chat.render(texte, True, (100, 100, 100))

        surface.blit(rendu_input, (self.chat_input_rect.x + 10, self.chat_input_rect.y + 10))

    def draw_instructions(self, surface):
        lignes = [
            "[Z,Q,S,D] DEPLACEMENT",
            "[T]       COMMUNICATION",
            "[E]       ACCEDER A LA BORNE"
        ]

        if self.is_host:
            if len(self.players) >= self.min_players_to_start:
                lignes.append("[G]       INITIALISER LE PROTOCOLE (LANCER)")
            else:
                lignes.append(f"          EN ATTENTE DE SUJETS ({self.min_players_to_start} MINIMUM)")
        else:
            lignes.append("          EN ATTENTE DE L'ADMINISTRATEUR")

        x = 40
        y = self.hauteur - 70

        for ligne in lignes:
            rendu = self.font_small.render(ligne, True, (150, 150, 160))
            surface.blit(rendu, (x, y))
            y += 18

    def draw(self, surface):
        self.draw_background(surface)
        self.draw_title(surface)
        self.draw_player_count(surface)
        self.draw_room(surface)
        self.draw_players(surface)
        self.draw_chat(surface)
        self.draw_instructions(surface)