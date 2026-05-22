import pygame

class NPCMaster:
    def __init__(self, screen_width, screen_height):
        self.width = 80
        self.height = 100
        # Position du maitre du jeu
        self.rect = pygame.Rect(screen_width - 150, screen_height // 2 - 50, self.width, self.height)
        self.font = pygame.font.Font(None, 28)
        
        # Chargement de ton image
        try:
            img = pygame.image.load("assets/maitre_du_jeu.png").convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except FileNotFoundError:
            # Sécurité si l'image manque : un carré rose fluo pour que tu le remarques direct
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255)) 

    def draw(self, screen, player_rect):
        # Dessin de ton image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        # Interaction si le joueur s'approche (zone gonflée de 60 pixels autour de lui)
        if player_rect.colliderect(self.rect.inflate(60, 60)):
            txt = self.font.render("[E] PARLER AU MAITRE", True, (255, 255, 100))
            screen.blit(txt, (self.rect.x - 40, self.rect.y - 30))