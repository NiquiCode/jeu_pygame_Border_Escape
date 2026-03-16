import random


class DiceManager:
    def __init__(self):
        pass

    def lancer_de(self):
        """Lance un dé classique entre 1 et 6."""
        return random.randint(1, 6)

    def lancer_des_portes(self, couleurs_portes):
        """
        Lance tous les dés correspondant aux portes disponibles.

        Entrée :
            couleurs_portes : liste de couleurs, ex ["rouge", "bleu", "vert"]

        Sortie :
            liste de dictionnaires avec couleur + résultat + capacité
        """
        resultats = []

        for couleur in couleurs_portes:
            valeur = self.lancer_de()
            resultats.append({
                "couleur": couleur,
                "resultat_de": valeur,
                "capacite": self.get_capacite_porte(valeur)
            })

        return resultats

    def get_capacite_porte(self, resultat_de):
        """
        Convertit le résultat du dé en nombre de joueurs autorisés.
        Ici, la capacité = résultat du dé.
        """
        return resultat_de

    def lancer_des_depuis_portes(self, portes):
        """
        Si vous avez déjà des objets porte avec un attribut couleur.

        Exemple :
            portes = [porte1, porte2, porte3]

        Retourne une liste de résultats pour chaque porte.
        """
        resultats = []

        for porte in portes:
            valeur = self.lancer_de()
            resultats.append({
                "porte": porte,
                "couleur": porte.couleur,
                "resultat_de": valeur,
                "capacite": self.get_capacite_porte(valeur)
            })

        return resultats

    def choisir_salle_cible(self):
        """
        Choisit une coordonnée aléatoire sur la map 3x3.
        """
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        return [x, y]

    def choisir_joueurs_requis(self, nombre_joueurs):
        """
        Choisit aléatoirement le nombre de joueurs requis.
        """
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
        return {
            "portes": self.lancer_des_portes(couleurs_portes),
            "salle_cible": self.choisir_salle_cible(),
            "joueurs_requis": self.choisir_joueurs_requis(nombre_joueurs)
        }