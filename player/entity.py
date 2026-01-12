import pygame

class PlayerEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        # Création du carré visuel (30x30 pixels)
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Vitesse de déplacement
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)

    def update_color(self, color):
        """Change la couleur du pion selon le joueur actif"""
        self.image.fill(color)

    def handle_input(self):
        """Gestion des touches ZQSD ou Flèches"""
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed

    def update(self):
        self.handle_input()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Empêcher de sortir de l'écran (Limites 1000x700)
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1000: self.rect.right = 1000
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 700: self.rect.bottom = 700