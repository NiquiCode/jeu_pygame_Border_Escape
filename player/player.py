class Player:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
        self.score = 0
        self.vies = 10 

    def gagner_points(self, points):
        self.score += points
        
    def perdre_points(self, points):
        self.score -= points
        if self.score < 0: self.score = 0

    def perdre_vie(self):
        self.vies -= 1

    def reset(self):
        #Remet le joueur full vie quand il meurt
        self.vies = 10
        self.score = 0