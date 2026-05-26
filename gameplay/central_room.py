import pygame
from player.dice import DiceManager

class CentralRoom:
    def __init__(self, screen_width, screen_height, map_manager, client=None):
        self.width = screen_width
        self.height = screen_height
        self.map_manager = map_manager
        self.client = client
        self.table_rect = pygame.Rect(screen_width//2 - 60, screen_height//2 - 50, 120, 100)
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = "Aucun objectif" # Variable synchronisée pour le HUD
        self.door_dice_results = []
        self.exit_portal_rect = pygame.Rect(screen_width//2 - 40, screen_height//2 - 40, 80, 80)
        self.font_prompt = pygame.font.SysFont("consolas", 24, True)

    def reset_round(self):
        self.dice_rolled = False
        self.door_dice_results = []
        
    def _format_target_name(self, coords):
        if not coords: return "Inconnu"
        lettre = chr(65 + int(coords[0]))
        chiffre = str(int(coords[1]) + 1)
        return f"Salle {lettre}{chiffre}"

    def roll_dice(self, total_players):
        res = DiceManager().lancer_systeme_des(total_players, ["rouge", "bleu", "vert", "jaune"])
        self.target_coords = res.get("salle_cible")
        self.target_name = self._format_target_name(self.target_coords)
        self.required_players = res.get("joueurs_requis", 1)
        
        doors = res.get("portes", [])
        for p in doors: p["ouverte"] = False
        self.door_dice_results = doors
        self.dice_rolled = True
        return res

    def apply_dice_result(self, data):
        self.door_dice_results = data.get("portes", [])
        for p in self.door_dice_results:
            if "ouverte" not in p: p["ouverte"] = False
            
        self.target_coords = tuple(data.get("salle_cible")) if data.get("salle_cible") else None
        self.target_name = self._format_target_name(self.target_coords)
        self.required_players = data.get("joueurs_requis", 1)
        self.dice_rolled = True

    def open_door(self, index):
        if 0 <= index < len(self.door_dice_results):
            self.door_dice_results[index]["ouverte"] = True

    def update(self, player, players_in_same_room, is_my_turn, roller_name, can_roll_dice=True):
        if self.map_manager.exit_revealed and list(self.map_manager.player_pos) == list(self.map_manager.exit_pos):
            if player.rect.colliderect(self.exit_portal_rect):
                return "FIN_DU_JEU"

        if is_my_turn and player.est_bloque and not self.dice_rolled:
            player.x = self.width//2 - player.size//2
            player.y = self.height//2 + 60
            player.rect.topleft = (player.x, player.y)

        if player.rect.colliderect(self.table_rect.inflate(60, 60)):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] and not self.dice_rolled and is_my_turn and can_roll_dice: 
                return "START_ROLL"
        
        if self.dice_rolled and self.door_dice_results:
            grid_size = getattr(self.map_manager, "grid_size", 3)
            x, y = self.map_manager.player_pos
            
            for i, porte in enumerate(self.door_dice_results):
                pos = str(porte.get("position") or porte.get("direction") or porte.get("pos", "")).lower()
                
                # SÉCURITÉ ABSOLUE : Blocage des portes hors-carte (Pas de collision possible)
                if pos in ("haut", "n", "up", "north") and y <= 0: continue
                if pos in ("bas", "s", "down", "south") and y >= grid_size - 1: continue
                if pos in ("gauche", "o", "w", "left", "west") and x <= 0: continue
                if pos in ("droite", "e", "right", "east") and x >= grid_size - 1: continue

                longueur, epaisseur = 120, 20
                rect_porte = None
                
                if pos in ("haut", "n", "up", "north"): rect_porte = pygame.Rect(self.width//2 - longueur//2, 0, longueur, epaisseur)
                elif pos in ("bas", "s", "down", "south"): rect_porte = pygame.Rect(self.width//2 - longueur//2, self.height - epaisseur, longueur, epaisseur)
                elif pos in ("gauche", "o", "w", "left", "west"): rect_porte = pygame.Rect(0, self.height//2 - longueur//2, epaisseur, longueur)
                elif pos in ("droite", "e", "right", "east"): rect_porte = pygame.Rect(self.width - epaisseur, self.height//2 - longueur//2, epaisseur, longueur)
                
                if rect_porte and player.rect.colliderect(rect_porte):
                    if not porte.get("ouverte", False):
                        player.perdre_vie()
                        porte["ouverte"] = True
                        if self.client: self.client.send({"type": "DOOR_OPENED", "index": i})
                        
                    if player.vies <= 0: return "MORT"
                    
                    if pos in ("haut", "n", "up", "north"): self.map_manager.player_pos[1] -= 1; player.y = self.height - player.size - 50
                    elif pos in ("bas", "s", "down", "south"): self.map_manager.player_pos[1] += 1; player.y = 50
                    elif pos in ("gauche", "o", "w", "left", "west"): self.map_manager.player_pos[0] -= 1; player.x = self.width - player.size - 50
                    elif pos in ("droite", "e", "right", "east"): self.map_manager.player_pos[0] += 1; player.x = 50
                    
                    player.rect.topleft = (player.x, player.y)
                    return "DOOR_CROSSED"
        
        if self.dice_rolled and self.target_coords:
            p_pos = [int(p) for p in self.map_manager.player_pos]
            t_pos = [int(p) for p in self.target_coords]
            if p_pos == t_pos and players_in_same_room >= self.required_players: 
                return "LANCER_ENIGME"
        return "CENTRAL"

    def draw(self, screen, is_my_turn=False, roller_name=""):
        pygame.draw.rect(screen, (80, 50, 20), self.table_rect, border_radius=10)
        pygame.draw.rect(screen, (120, 80, 40), self.table_rect, 3, border_radius=10)

        if not self.dice_rolled:
            if is_my_turn:
                prompt = self.font_prompt.render("[E] Lancer les dés", True, (0, 255, 0))
                screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height//2 - 80))
            else:
                prompt = self.font_prompt.render(f"En attente de {roller_name}...", True, (200, 200, 200))
                screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height//2 - 80))

        if self.dice_rolled and self.door_dice_results:
            grid_size = getattr(self.map_manager, "grid_size", 3)
            x, y = self.map_manager.player_pos
            
            for porte in self.door_dice_results:
                pos = str(porte.get("position") or porte.get("direction") or porte.get("pos", "")).lower()
                
                # SÉCURITÉ ABSOLUE : Blocage des portes hors-carte (Pas de dessin)
                if pos in ("haut", "n", "up", "north") and y <= 0: continue
                if pos in ("bas", "s", "down", "south") and y >= grid_size - 1: continue
                if pos in ("gauche", "o", "w", "left", "west") and x <= 0: continue
                if pos in ("droite", "e", "right", "east") and x >= grid_size - 1: continue

                longueur, epaisseur = 120, 20
                rect_porte = None
                
                if pos in ("haut", "n", "up", "north"): rect_porte = pygame.Rect(self.width//2 - longueur//2, 0, longueur, epaisseur)
                elif pos in ("bas", "s", "down", "south"): rect_porte = pygame.Rect(self.width//2 - longueur//2, self.height - epaisseur, longueur, epaisseur)
                elif pos in ("gauche", "o", "w", "left", "west"): rect_porte = pygame.Rect(0, self.height//2 - longueur//2, epaisseur, longueur)
                elif pos in ("droite", "e", "right", "east"): rect_porte = pygame.Rect(self.width - epaisseur, self.height//2 - longueur//2, epaisseur, longueur)
                
                if rect_porte:
                    color = (100, 200, 100) if porte.get("ouverte", False) else (200, 50, 50)
                    pygame.draw.rect(screen, color, rect_porte)