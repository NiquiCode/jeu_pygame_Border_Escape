import pygame


class LivesManager:
    def __init__(self, max_vies=10):
        self.max_vies = max_vies

        # Polices
        self.police_normale = pygame.font.Font(None, 28)
        self.police_titre = pygame.font.Font(None, 36)

        # Couleurs
        self.ROUGE = (231, 76, 60)
        self.BLANC = (255, 255, 255)
        self.GRIS = (50, 50, 70)
        self.GRIS_VIDE = (120, 120, 120)
        self.GRIS_BORD = (90, 90, 110)
        self.NOIR_TRANSPARENT = (20, 20, 30)

    # -------------------------
    # OUTILS INTERNES
    # -------------------------

    def _clamp_vies(self, joueur):
        """
        Garantit que les vies du joueur restent entre 0 et max_vies.
        """
        if joueur.vies < 0:
            joueur.vies = 0
        elif joueur.vies > self.max_vies:
            joueur.vies = self.max_vies

    # -------------------------
    # GESTION DES VIES
    # -------------------------

    def initialiser_vies(self, joueur):
        """Met les vies du joueur au maximum."""
        joueur.vies = self.max_vies
        self._clamp_vies(joueur)

    def perdre_vie(self, joueur, nb=1):
        """Retire nb vies au joueur sans descendre sous 0."""
        joueur.vies -= nb
        self._clamp_vies(joueur)

    def ajouter_vie(self, joueur, nb=1):
        """Ajoute nb vies au joueur sans dépasser max_vies."""
        joueur.vies += nb
        self._clamp_vies(joueur)

    def perte_entree_salle(self, joueur):
        """
        Le premier joueur qui entre dans une salle nouvellement ouverte
        perd 1 vie.
        """
        self.perdre_vie(joueur, 1)

    def perte_rester_meme_salle(self, joueur):
        """
        Un joueur qui reste dans la même salle d'un tour à l'autre
        perd 1 vie.
        """
        self.perdre_vie(joueur, 1)

    def perte_blocage_solitude(self, joueur):
        """
        Un joueur seul et bloqué dans une salle perd 1 vie par tour.
        """
        self.perdre_vie(joueur, 1)

    def est_elimine(self, joueur):
        """Retourne True si le joueur n'a plus de vies."""
        return joueur.vies <= 0

    def verifier_elimination(self, joueur):
        """Même rôle que est_elimine, nom plus explicite."""
        return self.est_elimine(joueur)

    def reset_joueur(self, joueur):
        """Remet le joueur à l'état de départ."""
        joueur.vies = self.max_vies
        joueur.score = getattr(joueur, "score", 0)
        joueur.score = 0
        self._clamp_vies(joueur)

    # -------------------------
    # GESTION DU BLOCAGE
    # -------------------------

    def joueur_est_seul(self, salle):
        """
        Retourne True si la salle contient exactement un joueur.
        On suppose que salle.joueurs est une liste.
        """
        return len(salle.joueurs) == 1

    def salle_occupee(self, salle):
        """Retourne True si la salle contient au moins un joueur."""
        return len(salle.joueurs) > 0

    def joueur_bloque_seul(self, index_salle, salles):
        """
        Règle :
        - si un joueur est seul dans une salle
        - il ne peut lancer les dés
        - il est libéré seulement si les 2 salles adjacentes sont occupées

        Retourne True si le joueur est bloqué.
        """
        salle_actuelle = salles[index_salle]

        if not self.joueur_est_seul(salle_actuelle):
            return False

        salle_gauche = salles[index_salle - 1] if index_salle > 0 else None
        salle_droite = salles[index_salle + 1] if index_salle < len(salles) - 1 else None

        if salle_gauche is None or salle_droite is None:
            return True

        if self.salle_occupee(salle_gauche) and self.salle_occupee(salle_droite):
            return False

        return True

    def appliquer_blocage_solitude(self, index_salle, salles):
        """
        Si un joueur est seul et bloqué, il perd 1 vie.
        Retourne le joueur concerné, sinon None.
        """
        salle_actuelle = salles[index_salle]

        if self.joueur_bloque_seul(index_salle, salles):
            joueur = salle_actuelle.joueurs[0]
            self.perte_blocage_solitude(joueur)
            return joueur

        return None

    # -------------------------
    # AFFICHAGE PYGAME
    # -------------------------

    def afficher_vies(self, ecran, joueur, x_pos=20, y_pos=210):
        """
        Affiche le panneau de vies du joueur.
        """
        width = 300
        height = 95

        fond_rect = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(ecran, self.GRIS, fond_rect, border_radius=12)
        pygame.draw.rect(ecran, self.GRIS_BORD, fond_rect, 2, border_radius=12)

        texte_titre = self.police_titre.render("Vies", True, self.BLANC)
        ecran.blit(texte_titre, (x_pos + 12, y_pos + 8))

        texte_nom = self.police_normale.render(joueur.nom, True, self.BLANC)
        ecran.blit(texte_nom, (x_pos + 12, y_pos + 40))

        vies_affichees = max(0, min(joueur.vies, self.max_vies))
        texte_chiffre = self.police_normale.render(
            f"{vies_affichees}/{self.max_vies}",
            True,
            self.BLANC
        )
        ecran.blit(texte_chiffre, (x_pos + width - 75, y_pos + 40))

        x_coeur = x_pos + 12
        y_coeur = y_pos + 67

        for i in range(self.max_vies):
            if i < vies_affichees:
                texte_coeur = self.police_normale.render("♥", True, self.ROUGE)
            else:
                texte_coeur = self.police_normale.render("♡", True, self.GRIS_VIDE)

            ecran.blit(texte_coeur, (x_coeur, y_coeur))
            x_coeur += 23