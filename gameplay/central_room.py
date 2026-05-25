import pygame
from player.dice import DiceManager

class CentralRoom:
    def __init__(self, screen_width, screen_height, map_manager, client=None):
        self.width, self.height = screen_width, screen_height
        self.map_manager, self.client = map_manager, client
        self.table_rect = pygame.Rect(screen_width//2 - 60, screen_height//2 - 50, 120, 100)
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
        self.door_dice_results = []
        self.font = pygame.font.Font(None, 32)

    def reset_round(self):
        self.dice_rolled = False
        self.target_coords = None
        self.target_name = ""
        self.required_players = 0
        self.door_dice_results = []

    def roll_dice(self, total_players):
        # CORRECTION : On envoie bien 4 couleurs pour générer les 4 portes !
        res = DiceManager().lancer_systeme_des(total_players, ["rouge", "bleu", "vert", "jaune"])
        self.target_coords = res.get("salle_cible")
        self.required_players = res.get("joueurs_requis", 1)
        if self.target_coords and self.map_manager:
            self.target_name = self.map_manager.get_coordinates_str(self.target_coords[0], self.target_coords[1])
        else:
            self.target_name = ""
        self.door_dice_results = res.get("portes", [])
        self.dice_rolled = True
        return res

    def apply_dice_result(self, data):
        self.door_dice_results = data.get("portes", [])
        self.target_coords = tuple(data.get("salle_cible")) if data.get("salle_cible") else None
        if self.target_coords and self.map_manager:
            self.target_name = self.map_manager.get_coordinates_str(self.target_coords[0], self.target_coords[1])
        else:
            self.target_name = ""
        self.required_players = data.get("joueurs_requis", 1)
        self.dice_rolled = True

    def update(self, player, players_in_same_room, is_my_turn, roller_name, can_roll_dice=True):
        if player.rect.colliderect(self.table_rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] and not self.dice_rolled and is_my_turn and can_roll_dice: 
                return "START_ROLL"
        
        # LOGIQUE DE TRANSITION : Permet au joueur de traverser les portes
        if self.dice_rolled and self.door_dice_results:
            for porte in self.door_dice_results:
                pos = porte.get("position") or porte.get("direction") or porte.get("pos")
                if not pos: continue
                pos = str(pos).lower()
                
                # Portes plus fines et esthétiques
                longueur, epaisseur = 100, 15
                rect_porte = None
                
                # CORRECTION DU BUG : Utilisation de "in" partout pour éviter la disparition
                if pos in ("haut", "n", "up", "north"): 
                    rect_porte = pygame.Rect(self.width//2 - longueur//2, 0, longueur, epaisseur)
                elif pos in ("bas", "s", "down", "south"): 
                    rect_porte = pygame.Rect(self.width//2 - longueur//2, self.height - epaisseur, longueur, epaisseur)
                elif pos in ("gauche", "o", "w", "left", "west"): 
                    rect_porte = pygame.Rect(0, self.height//2 - longueur//2, epaisseur, longueur)
                elif pos in ("droite", "e", "right", "east"): 
                    rect_porte = pygame.Rect(self.width - epaisseur, self.height//2 - longueur//2, epaisseur, longueur)
                
                # Collision physique avec la porte
                if rect_porte and player.rect.colliderect(rect_porte):
                    if pos in ("haut", "n", "up", "north"):
                        self.map_manager.player_pos[1] -= 1
                        player.y = self.height - player.size - 40
                    elif pos in ("bas", "s", "down", "south"):
                        self.map_manager.player_pos[1] += 1
                        player.y = 40
                    elif pos in ("gauche", "o", "w", "left", "west"):
                        self.map_manager.player_pos[0] -= 1
                        player.x = self.width - player.size - 40
                    elif pos in ("droite", "e", "right", "east"):
                        self.map_manager.player_pos[0] += 1
                        player.x = 40
                    
                    player.rect.topleft = (player.x, player.y)
                    
                    if self.client:
                        self.client.send({
                            "type": "PLAYER_STATE", "id": player.player_id, "nom": player.nom,
                            "x": player.x, "y": player.y, "score": player.score, "vies": player.vies,
                            "room_pos": self.map_manager.player_pos[:]
                        })
        
        if self.dice_rolled and self.target_coords:
            p_pos = [int(p) for p in self.map_manager.player_pos]
            t_pos = [int(p) for p in self.target_coords]
            if p_pos == t_pos and players_in_same_room >= self.required_players: 
                return "LANCER_ENIGME"
        return "CENTRAL"

    def draw(self, screen):
        # Table centrale
        pygame.draw.rect(screen, (100, 60, 20), self.table_rect)
        
        longueur, epaisseur = 100, 15
        
        if not self.dice_rolled:
            txt = self.font.render("Table (E) : Lancer le dé", True, (255, 255, 255))
            screen.blit(txt, (self.width // 2 - txt.get_width() // 2, self.height // 2 - 80))
            
            # Portes grises fermées par défaut
            pygame.draw.rect(screen, (80, 80, 80), (self.width//2 - longueur//2, 0, longueur, epaisseur))
            pygame.draw.rect(screen, (80, 80, 80), (self.width//2 - longueur//2, self.height - epaisseur, longueur, epaisseur))
            pygame.draw.rect(screen, (80, 80, 80), (0, self.height//2 - longueur//2, epaisseur, longueur))
            pygame.draw.rect(screen, (80, 80, 80), (self.width - epaisseur, self.height//2 - longueur//2, epaisseur, longueur))
        else:
            # Portes colorées et ouvertes après le lancer
            for porte in self.door_dice_results:
                pos = porte.get("position") or porte.get("direction") or porte.get("pos")
                if not pos: continue
                pos = str(pos).lower()
                
                couleur_nom = porte.get("couleur") or porte.get("color") or "gris"
                couleurs = {
                    "rouge": (220, 20, 20), 
                    "bleu": (20, 100, 220), 
                    "vert": (20, 200, 20), 
                    "jaune": (220, 200, 20), # On a ajouté la 4ème couleur ici aussi !
                    "gris": (150, 150, 150)
                }
                c = couleurs.get(str(couleur_nom).lower(), (150, 150, 150))
                
                rect_porte = None
                if pos in ("haut", "n", "up", "north"): 
                    rect_porte = pygame.Rect(self.width//2 - longueur//2, 0, longueur, epaisseur)
                elif pos in ("bas", "s", "down", "south"): 
                    rect_porte = pygame.Rect(self.width//2 - longueur//2, self.height - epaisseur, longueur, epaisseur)
                elif pos in ("gauche", "o", "w", "left", "west"): 
                    rect_porte = pygame.Rect(0, self.height//2 - longueur//2, epaisseur, longueur)
                elif pos in ("droite", "e", "right", "east"): 
                    rect_porte = pygame.Rect(self.width - epaisseur, self.height//2 - longueur//2, epaisseur, longueur)
                
                if rect_porte:
                    pygame.draw.rect(screen, c, rect_porte)
                    pygame.draw.rect(screen, (255, 255, 255), rect_porte, 2)