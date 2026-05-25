import pygame

class NPCMaster:
    def __init__(self, screen_width, screen_height):
        """
        Initialise le Maître du Jeu en tant qu'image chargée depuis le disque.
        """
        # --- MODIFICATION ---
        # Définition des dimensions et de la position pour le nouveau PNJ
        # Ce PNJ est basé sur une image chargée, et non plus sur des formes géométriques.
        #
        self.width = 180
        self.height = 200
        # Positionné à droite de la salle
        self.rect = pygame.Rect(screen_width - 250, screen_height // 2 - 100, self.width, self.height)
        
        self.font = pygame.font.Font(None, 28)
        self.talking = False

        # --- NOUVEAU : Chargement de l'image personnalisée ---
        try:
            # Nous chargeons l'image que vous avez dessinée et que vous nommerez
            # "maitre_du_jeu2.png" dans le dossier "assets/".
            #
            img = pygame.image.load("assets/maitre_du_jeu2.png").convert_alpha()
            # On redimensionne l'image pour qu'elle corresponde aux dimensions de self.rect
            #
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except FileNotFoundError:
            # Sécurité en cas de fichier manquant : on crée une surface distinctive
            # (un carré rose fluo) pour signaler le problème.
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255)) 

    def draw(self, screen, player_rect):
        """
        Dessine le PNJ (votre image) et gère l'indication d'interaction.
        """
        # --- MODIFICATION ---
        # 1. On dessine l'image chargée au lieu des formes géométriques.
        #
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        # 2. On conserve et on adapte la logique d'interaction
        # On vérifie la proximité entre le joueur et le rectangle du nouveau PNJ.
        # On utilise la même logique d'inflation pour la détection que dans le main.py.
        #
        if player_rect.colliderect(self.rect.inflate(60, 60)):
            # Si le joueur est proche, on affiche le texte d'indication.
            #
            txt = self.font.render("[E] PARLER AU MAITRE", True, (255, 255, 100))
            # On positionne le texte par rapport au rectangle du PNJ.
            #
            screen.blit(txt, (self.rect.x + 10, self.rect.y - 30))