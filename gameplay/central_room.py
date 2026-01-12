import pygame
import random
from player.entity import PlayerEntity

class CentralRoom:
    def __init__(self, screen_width, screen_height, map_manager):
        self.width = screen_width
        self.height = screen_height
        self.map_manager = map_manager 
        
        self.player_sprite = PlayerEntity(screen_width // 2, screen_height // 2, (255, 255, 255))
        self.sprite_group = pygame.sprite.GroupSingle(self.player_sprite)

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
        self.target_coords = None # [x, y]
        self.target_name = ""     # "A1"
        self.required_players = 0
        self.players_arrived_count = 0 # Combien de joueurs sont arrivés dans la salle cible
        
        self.message = "Table (E) : Lancer les dés"
        self.font = pygame.font.Font(None, 32)
        self.font_big = pygame.font.Font(None, 40)

    def roll_dice(self, total_players_in_game):
        """Lance les dés pour définir la destination et la contrainte"""
        # 1. Coordonnées Aléatoires
        tx = random.randint(0, 2)
        ty = random.randint(0, 2)
        self.target_coords = [tx, ty]
        self.target_name = self.map_manager.get_coordinates_str(tx, ty)
        
        # 2. Nombre de joueurs requis (Max = nb joueurs total)
        self.required_players = random.randint(1, total_players_in_game)
        
        self.dice_rolled = True
        self.players_arrived_count = 0 # Reset du compteur d'arrivée
        self.update_message()

    def update_message(self):
        if not self.dice_rolled:
            self.message = "Table (E) : Lancer les dés"
        else:
            self.message = f"CIBLE: {self.target_name} | JOUEURS REQUIS: {self.required_players}"

    def reset_round(self):
        """Appelé après une réussite d'énigme"""
        self.dice_rolled = False
        self.target_coords = None
        self.players_arrived_count = 0
        self.update_message()

    def check_doors_availability(self):
        px, py = self.map_manager.player_pos
        available = []
        if py > 0: available.append("HAUT")
        if py < 2: available.append("BAS")
        if px > 0: available.append("GAUCHE")
        if px < 2: available.append("DROITE")
        return available

    def update(self, current_player_obj):
        """
        current_player_obj : L'objet Player (Données) pour gérer la vie
        """
        self.player_sprite.update_color(current_player_obj.couleur)
        self.sprite_group.update()
        
        keys = pygame.key.get_pressed()
        
        # --- TABLE (Lancer les dés) ---
        if self.player_sprite.rect.colliderect(self.table_rect):
            # On ne peut lancer que si pas déjà lancé
            if keys[pygame.K_e] and not self.dice_rolled:
                # On assume 3 joueurs max pour l'instant (ou len(joueurs) dans le main)
                self.roll_dice(3) 

        # --- PORTES (Déplacement) ---
        available_doors = self.check_doors_availability()
        
        for direction, rect in self.doors.items():
            if direction in available_doors and self.player_sprite.rect.colliderect(rect):
                
                # Le joueur franchit une porte -> PERD 1 VIE
                current_player_obj.perdre_vie()
                print(f"-1 Vie pour déplacement. Reste: {current_player_obj.vies}")
                
                # Déplacement Map
                moved = self.map_manager.move_player(direction)
                
                if moved:
                    # Repositionnement visuel
                    if direction == "HAUT": self.player_sprite.rect.y = self.height - 60
                    if direction == "BAS": self.player_sprite.rect.y = 60
                    if direction == "GAUCHE": self.player_sprite.rect.x = self.width - 60
                    if direction == "DROITE": self.player_sprite.rect.x = 60
                    
                    # --- VÉRIFICATION LOGIQUE ---
                    current_pos = self.map_manager.player_pos
                    
                    # 1. Est-ce la SORTIE ? (Si visible)
                    if current_pos == self.map_manager.exit_pos and self.map_manager.exit_revealed:
                        return "FIN_DU_JEU"

                    # 2. Est-ce la salle CIBLE des dés ?
                    if self.dice_rolled and current_pos == self.target_coords:
                        # Un joueur est arrivé !
                        self.players_arrived_count += 1
                        print(f"Arrivé cible ! Compteur: {self.players_arrived_count}/{self.required_players}")
                        
                        # A-t-on assez de joueurs ?
                        if self.players_arrived_count >= self.required_players:
                            return "LANCER_ENIGME"
                        else:
                            self.message = f"En attente... ({self.players_arrived_count}/{self.required_players} joueurs)"
                    else:
                        # Mauvaise salle ou pas de dés lancés
                        pass

        return "CENTRAL"

    def draw(self, screen):
        # Fond couleur salle
        room_color = self.map_manager.get_current_room_color()
        bg_color = (room_color[0]//2, room_color[1]//2, room_color[2]//2)
        screen.fill(bg_color)

        # Portes
        available = self.check_doors_availability()
        for direction in available:
            pygame.draw.rect(screen, (50, 50, 50), self.doors[direction])

        # Table
        pygame.draw.rect(screen, (100, 60, 20), self.table_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.table_rect, 2)
        
        # Message Info
        text = self.font.render(self.message, True, (255, 255, 255))
        screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - 80))
        
        # Afficher coordonnées actuelles en gros au fond
        coord_txt = self.map_manager.get_coordinates_str(self.map_manager.player_pos[0], self.map_manager.player_pos[1])
        lbl = self.font_big.render(coord_txt, True, (255, 255, 255))
        lbl.set_alpha(100)
        screen.blit(lbl, (50, 50))

        # Joueur
        self.sprite_group.draw(screen)