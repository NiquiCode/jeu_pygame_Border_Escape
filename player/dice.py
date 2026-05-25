import random

class DiceManager:
    def __init__(self):
        self.map_min_x = 0
        self.map_max_x = 2
        self.map_min_y = 0
        self.map_max_y = 2
        self.central_room = [1, 1]

    def lancer_de(self):
        return random.randint(1, 6)

    def get_capacite_porte(self, resultat_de):
        return max(1, int(resultat_de))

    def lancer_des_portes(self, couleurs_portes):
        if not couleurs_portes:
            return []

        resultats = []
        # Liste des positions physiques pour correspondre à CentralRoom
        positions = ["haut", "bas", "gauche", "droite"]
        
        for i, couleur in enumerate(couleurs_portes):
            valeur = self.lancer_de()
            # On attribue une position unique à chaque porte de la liste
            pos = positions[i % len(positions)]
            
            resultats.append({
                "couleur": couleur,
                "position": pos,
                "nom": f"Salle {pos.upper()}",
                "resultat_de": valeur,
                "capacite": self.get_capacite_porte(valeur)
            })

        return resultats

    def lancer_des_depuis_portes(self, portes):
        if not portes:
            return []

        resultats = []
        positions = ["haut", "bas", "gauche", "droite"]
        for i, porte in enumerate(portes):
            valeur = self.lancer_de()
            couleur = getattr(porte, "couleur", "inconnue")
            pos = positions[i % len(positions)]

            resultats.append({
                "porte": porte,
                "couleur": couleur,
                "position": pos,
                "nom": f"Salle {pos.upper()}",
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
        salles = self._toutes_les_salles_possibles()
        if exclure_centre:
            salles = [s for s in salles if s != self.central_room]
        if not salles:
            return self.central_room[:]
        return random.choice(salles)

    def choisir_joueurs_requis(self, nombre_joueurs):
        try:
            nombre_joueurs = int(nombre_joueurs)
        except (TypeError, ValueError):
            nombre_joueurs = 1
        nombre_joueurs = max(1, nombre_joueurs)
        return random.randint(1, nombre_joueurs)

    def lancer_systeme_des(self, nombre_joueurs, couleurs_portes):
        portes = self.lancer_des_portes(couleurs_portes)
        salle_cible = self.choisir_salle_cible(exclure_centre=True)
        joueurs_requis = self.choisir_joueurs_requis(nombre_joueurs)

        return {
            "portes": portes,
            "salle_cible": salle_cible,
            "joueurs_requis": joueurs_requis
        }