#Rôle :
# - Initialiser PyGame
# - Gérer les événements globaux (quitter le jeu)
# - Appeler les méthodes update() et draw() du GameManager

import pygame
import sys
from player.player import Joueur
from gameplay.scoring import ScoringSystem
from player.lives_manager import LivesManager
from ui.hud import HUD
from ui.end_screen import EndScreen

#Initialisation
pygame.init()

#Constantes
LARGEUR = 1000
HAUTEUR = 700
FPS = 60

#Écran
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Border Escape - PoC Scoring")
horloge = pygame.time.Clock()

#Couleurs
NOIR = (15, 15, 30)
BLEU = (52, 152, 219)
ROSE = (255, 105, 180)
VERT = (46, 204, 113)

#Création des systèmes
scoring_system = ScoringSystem()
lives_manager = LivesManager()
hud = HUD(LARGEUR)
end_screen = EndScreen(LARGEUR, HAUTEUR)

#Création des joueurs
joueurs = [
    Joueur("Cédric", BLEU),
    Joueur("Alice", ROSE),
    Joueur("Bob", VERT)
]

joueur_actuel_index = 0
partie_terminee = False

#Boucle principale
en_cours = True
while en_cours:
    #Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        
        if event.type == pygame.KEYDOWN:
            #Touche R pour rejouer
            if event.key == pygame.K_r and partie_terminee:
                for joueur in joueurs:
                    joueur.vies = 10
                    joueur.score = 0
                joueur_actuel_index = 0
                partie_terminee = False
            
            #Touche F pour terminer (test)
            if event.key == pygame.K_f:
                partie_terminee = True
            
            #Touche ESPACE pour réussir énigme (test)
            if event.key == pygame.K_SPACE and not partie_terminee:
                scoring_system.recompenser_enigme_reussie(joueurs[joueur_actuel_index])
            
            #Touche X pour rater énigme (test)
            if event.key == pygame.K_x and not partie_terminee:
                scoring_system.penaliser_enigme_ratee(joueurs[joueur_actuel_index])
            
            #Touche C pour changer joueur (test)
            if event.key == pygame.K_c and not partie_terminee:
                joueur_actuel_index = (joueur_actuel_index + 1) % len(joueurs)
    
    #Affichage
    ecran.fill(NOIR)
    
    if not partie_terminee:
        #Afficher HUD
        scoring_system.afficher_hud_score(ecran, joueurs, joueur_actuel_index)
        lives_manager.afficher_vies(ecran, joueurs[joueur_actuel_index])
        hud.afficher_liste_joueurs(ecran, joueurs, joueur_actuel_index)
        
        #Instructions
        police = pygame.font.Font(None, 20)
        instructions = [
            "ESPACE = Réussir énigme (+100 pts)",
            "X = Rater énigme (-1 vie)",
            "C = Changer joueur",
            "F = Écran de fin"
        ]
        y = HAUTEUR - 120
        for texte in instructions:
            surface = police.render(texte, True, (200, 200, 200))
            ecran.blit(surface, (LARGEUR // 2 - 150, y))
            y += 25
    else:
        end_screen.afficher(ecran, joueurs)
    
    pygame.display.flip()
    horloge.tick(FPS)

pygame.quit()
sys.exit()