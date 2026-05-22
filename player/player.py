import pygame
import time

class Player:
    def __init__(self, nom, couleur, player_id=None, is_local=True, x=100, y=100, image_path=None):
        self.nom = nom
        self.couleur = tuple(couleur)
        self.score = 0
        self.vies = 10
        self.player_id = player_id
        self.is_local = is_local
        self.is_host = False
        
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.speed = 4
        self.facing_right = True
        
        self.image_path = image_path
        self.image = None
        self.charger_image()

        self.idle_animation_counter = 0
        self.idle_frames = [self.image] if self.image else []
        self.current_idle_frame = 0
        self.last_animation_time = time.time()

    def charger_image(self):
        img_path = self.image_path if self.image_path else "assets/perso1.png"
        try:
            img = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
            self.idle_frames = [self.image]
        except FileNotFoundError:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255))
            self.idle_frames = [self.image]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy, min_x=0, max_x=1000, min_y=0, max_y=700):
        old_x = self.x
        self.x += dx
        self.y += dy

        if self.x > old_x:
            self.facing_right = True
        elif self.x < old_x:
            self.facing_right = False

        self.x = max(min_x, min(max_x - self.width, self.x))
        self.y = max(min_y, min(max_y - self.height, self.y))

    def gagner_points(self, points):
        self.score += points

    def perdre_points(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0

    def perdre_vie(self):
        self.vies -= 1
        if self.vies < 0:
            self.vies = 0

    def reset(self):
        self.vies = 10
        self.score = 0
        self.x = 220
        self.y = 360

    def update(self):
        now = time.time()
        if now - self.last_animation_time > 0.5:
            if len(self.idle_frames) > 0:
                self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_frames)
            self.last_animation_time = now

    def draw(self, screen, font, actif=False):
        if not self.idle_frames:
            return
            
        img_to_blit = self.idle_frames[self.current_idle_frame]
        
        if not self.facing_right:
            img_to_blit = pygame.transform.flip(img_to_blit, True, False)
            correction_pixels = 8 
            screen.blit(img_to_blit, (self.x + correction_pixels, self.y))
        else:
            screen.blit(img_to_blit, (self.x, self.y))

        texte = font.render(self.nom, True, (255, 255, 255))
        texte_rect = texte.get_rect(center=(self.x + self.width // 2, self.y - 10))
        screen.blit(texte, texte_rect)

    def to_dict(self):
        return {
            "id": self.player_id,
            "nom": self.nom,
            "x": self.x,
            "y": self.y,
            "score": self.score,
            "vies": self.vies,
            "couleur": list(self.couleur),
            "facing_right": self.facing_right,
            "is_host": self.is_host,
            "image_path": self.image_path
        }

    def update_from_dict(self, data):
        old_x = self.x
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.score = data.get("score", self.score)
        self.vies = data.get("vies", self.vies)

        if "couleur" in data:
            self.couleur = tuple(data["couleur"])
            
        if "image_path" in data and data["image_path"] != self.image_path:
            self.image_path = data["image_path"]
            self.charger_image()

        if "facing_right" in data:
            self.facing_right = data["facing_right"]
        else:
            if self.x > old_x:
                self.facing_right = True
            elif self.x < old_x:
                self.facing_right = False

        if "is_host" in data:
            self.is_host = data["is_host"]