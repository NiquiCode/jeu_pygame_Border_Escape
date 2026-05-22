import pygame

class WorldManager:
    def __init__(self):
        nom_image = "assets/sol.png"
        try:
            self.large_floor_image = pygame.image.load(nom_image).convert()
            self.large_floor_image = pygame.transform.scale(self.large_floor_image, (1000, 700))
        except FileNotFoundError:
            try:
                self.large_floor_image = pygame.image.load("assets/sol_grotte_pixel.png").convert()
                self.large_floor_image = pygame.transform.scale(self.large_floor_image, (1000, 700))
            except FileNotFoundError:
                print("🚨 ERREUR : Image de sol introuvable dans le dossier assets.")
                self.large_floor_image = pygame.Surface((1000, 700))
                self.large_floor_image.fill((30, 30, 30))

    def generate_world(self):
        pass

    def draw(self, screen):
        screen.blit(self.large_floor_image, (0, 0))