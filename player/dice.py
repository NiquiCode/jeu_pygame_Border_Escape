import random


class DiceManager:
    def __init__(self):
        self.map_min_x = 0
        self.map_max_x = 2
        self.map_min_y = 0
        self.map_max_y = 2
        self.central_room = [1, 1]

    def lancer_de(self):
        """Lance un dé classique entre 1 et 6."""
        return random.randint(1, 6)

    def get_capacite_porte(self, resultat_de):
        """
        Convertit le résultat du dé en nombre de joueurs autorisés.
        Ici, la capacité = résultat du dé.
        """
        return max(1, int(resultat_de))

    def lancer_des_portes(self, couleurs_portes):
        """
        Lance tous les dés correspondant aux portes disponibles.

        Entrée :
            couleurs_portes : liste de couleurs, ex ["rouge", "bleu", "vert"]

        Sortie :
            liste de dictionnaires avec couleur + résultat + capacité
        """
        if not couleurs_portes:
            return []

        resultats = []

        for couleur in couleurs_portes:
            valeur = self.lancer_de()
            resultats.append({
                "couleur": couleur,
                "resultat_de": valeur,
                "capacite": self.get_capacite_porte(valeur)
            })

        return resultats

    def lancer_des_depuis_portes(self, portes):
        """
        Si vous avez déjà des objets porte avec un attribut couleur.

        Exemple :
            portes = [porte1, porte2, porte3]

        Retourne une liste de résultats pour chaque porte.
        """
        if not portes:
            return []

        resultats = []

        for porte in portes:
            valeur = self.lancer_de()
            couleur = getattr(porte, "couleur", "inconnue")

            resultats.append({
                "porte": porte,
                "couleur": couleur,
                "resultat_de": valeur,
                "capacite": self.get_capacite_porte(valeur)
            })

        return resultats

    def _toutes_les_salles_possibles(self):
        salles = []

        for x in range(self.map_min_x, self.map_max_x + 1):
            for y in range(self.map_min_y, self.map_max_y + 1):
                salles.append([x, y])

        return salles

    def choisir_salle_cible(self, exclure_centre=True):
        """
        Choisit une coordonnée aléatoire sur la map 3x3.

        Par défaut, on exclut la salle centrale [1, 1],
        car la cible doit être une salle à atteindre, pas la salle de départ.
        """
        salles = self._toutes_les_salles_possibles()

        if exclure_centre:
            salles = [s for s in salles if s != self.central_room]

        if not salles:
            return self.central_room[:]

        return random.choice(salles)

    def choisir_joueurs_requis(self, nombre_joueurs):
        """
        Choisit aléatoirement le nombre de joueurs requis.

        Le résultat est borné entre 1 et nombre_joueurs.
        """
        try:
            nombre_joueurs = int(nombre_joueurs)
        except (TypeError, ValueError):
            nombre_joueurs = 1

        nombre_joueurs = max(1, nombre_joueurs)
        return random.randint(1, nombre_joueurs)

    def lancer_systeme_des(self, nombre_joueurs, couleurs_portes):
        """
        Lance tout le système de dés du tour.

        Retourne :
        {
            "portes": [...],
            "salle_cible": [x, y],
            "joueurs_requis": n
        }
        """
        portes = self.lancer_des_portes(couleurs_portes)
        salle_cible = self.choisir_salle_cible(exclure_centre=True)
        joueurs_requis = self.choisir_joueurs_requis(nombre_joueurs)

        return {
            "portes": portes,
            "salle_cible": salle_cible,
            "joueurs_requis": joueurs_requis
        }