import random

# Lance un dé (1 à 6)
def lancer_de():
    return random.randint(1, 6)


# Lance tous les dés des portes
def lancer_des_portes(couleurs_portes):
    resultats = {}

    for couleur in couleurs_portes:
        resultats[couleur] = lancer_de()

    return resultats
