import pygame
import sys

# --- IMPORTS ---
from player.player import Player  
from gameplay.scoring import ScoringSystem
from player.lives_manager import LivesManager
from gameplay.central_room import CentralRoom
from gameplay.map_manager import MapManager
from gameplay.puzzle_rooms import PuzzleRoom
from ui.hud import HUD
from ui.minimap import Minimap
from ui.end_screen import EndScreen
from ui.death_screen import DeathScreen

pygame.init()
LARGEUR, HAUTEUR = 1000, 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Border Escape - Full Game")
horloge = pygame.time.Clock()

# Systèmes
scoring_system = ScoringSystem()
lives_manager = LivesManager()
hud = HUD(LARGEUR)
end_screen = EndScreen(LARGEUR, HAUTEUR)
death_screen = DeathScreen(LARGEUR, HAUTEUR)

# Joueurs
joueurs = [
    Player("Cédric", (52, 152, 219)), 
    Player("Alice", (255, 105, 180)), 
    Player("Bob", (46, 204, 113))
]
joueur_actuel_index = 0

# Gameplay
map_manager = MapManager()
central_room = CentralRoom(LARGEUR, HAUTEUR, map_manager)
minimap = Minimap(LARGEUR, HAUTEUR, map_manager)

# Variable pour stocker l'énigme en cours
puzzle_actif = None 

partie_terminee = False
etat_jeu = "CENTRAL" # États : CENTRAL, ENIGME, MORT, FIN

while True:
    joueur_actif = joueurs[joueur_actuel_index]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        
        # --- GESTION ÉTAT : MORT ---
        if etat_jeu == "MORT":
            if death_screen.handle_input(event): # Si clic sur Rejouer
                joueur_actif.reset()       
                map_manager.generate_new_map() 
                central_room.reset_round()
                etat_jeu = "CENTRAL"
        
        # --- GESTION ÉTAT : ENIGME ---
        elif etat_jeu == "ENIGME" and puzzle_actif:
            resultat = puzzle_actif.handle_event(event)
            
            if resultat is True: # GAGNÉ
                print("Énigme réussie !")
                joueur_actif.gagner_points(100)
                map_manager.quests_completed += 1
                map_manager.check_exit_condition()
                central_room.reset_round() 
                etat_jeu = "CENTRAL"
                puzzle_actif = None

            elif resultat is False: # PERDU
                print("Énigme ratée...")
                joueur_actif.perdre_points(50)
                joueur_actif.perdre_vie()
                
                if joueur_actif.vies <= 0:
                    etat_jeu = "MORT"
                else:
                    puzzle_actif = PuzzleRoom() 

        # --- GESTION ÉTAT : CENTRAL ---
        elif etat_jeu == "CENTRAL":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    minimap.toggle()
                if event.key == pygame.K_c:
                    joueur_actuel_index = (joueur_actuel_index + 1) % len(joueurs)

    # --- UPDATE & DRAW ---
    if not partie_terminee:
        ecran.fill((0, 0, 0))

        # A. SALLE CENTRALE
        if etat_jeu == "CENTRAL":
            result = central_room.update(joueur_actif)
            central_room.draw(ecran)
            
            if joueur_actif.vies <= 0:
                etat_jeu = "MORT"

            elif result == "LANCER_ENIGME":
                puzzle_actif = PuzzleRoom()
                etat_jeu = "ENIGME"
            
            elif result == "FIN_DU_JEU":
                partie_terminee = True

        # B. ÉNIGME
        elif etat_jeu == "ENIGME" and puzzle_actif:
            puzzle_actif.draw(ecran)

        # C. MORT
        elif etat_jeu == "MORT":
            central_room.draw(ecran)
            death_screen.draw(ecran)

        # --- UI GLOBALE ---
        if etat_jeu != "MORT":
            # MODIFICATION ICI : On passe map_manager pour afficher les quêtes
            scoring_system.afficher_hud_score(ecran, joueurs, joueur_actuel_index, map_manager)
            lives_manager.afficher_vies(ecran, joueurs[joueur_actuel_index])
            minimap.draw(ecran)

    else:
        end_screen.afficher(ecran, joueurs)
    
    pygame.display.flip()
    horloge.tick(60)