import pygame


class Player:
    def __init__(self, nom, couleur, player_id=None, is_local=True, x=100, y=100):
        self.nom = nom
        self.couleur = couleur

        self.score = 0
        self.vies = 10

        # Préparation multijoueur
        self.player_id = player_id
        self.is_local = is_local

        # Position / taille pour affichage
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 4

    def gagner_points(self, points):
        self.score += points

    def perdre_points(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0

    def perdre_vie(self):
        self.vies -= 1

    def reset(self):
        # Remet le joueur full vie quand il meurt
        self.vies = 10
        self.score = 0

    def draw(self, screen, font, actif=False):
        # Dessin du joueur
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.couleur, rect)

        # Contour pour le joueur actif
        if actif:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

        # Affichage du pseudo au-dessus
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
            "vies": self.vies
        }

    def update_from_dict(self, data):
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.score = data.get("score", self.score)
        self.vies = data.get("vies", self.vies)