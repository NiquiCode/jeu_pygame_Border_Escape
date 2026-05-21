import pygame
from world.map_tiles import Tile

class WorldManager:
    def __init__(self):
        self.tiles = []
        self.taille_tuile = 50
        
        try:
            self.sol_image = pygame.image.load("assets/sol_grotte.jpg").convert()
            self.sol_image = pygame.transform.scale(self.sol_image, (self.taille_tuile, self.taille_tuile))
        except FileNotFoundError:
            print("Attention: Image assets/sol_grotte.jpg introuvable.")
            self.sol_image = pygame.Surface((self.taille_tuile, self.taille_tuile))
            self.sol_image.fill((30, 30, 30))

    def generate_world(self):
        self.tiles = []
        for x in range(20):
            for y in range(14):
                self.tiles.append(Tile(x * self.taille_tuile, y * self.taille_tuile, "sol"))

    def draw(self, screen):
        for tile in self.tiles:
            screen.blit(self.sol_image, (tile.x, tile.y))