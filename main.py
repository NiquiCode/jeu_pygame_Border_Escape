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
from ui.menu import LobbyMenu
from network.server import GameServer
from network.client import GameClient

pygame.init()
LARGEUR, HAUTEUR = 1000, 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Border Escape - Full Game")
horloge = pygame.time.Clock()

# Polices
font_joueur = pygame.font.SysFont(None, 24)
font_titre = pygame.font.SysFont(None, 52)
font_texte = pygame.font.SysFont(None, 36)
font_input = pygame.font.SysFont(None, 42)
font_loading = pygame.font.SysFont(None, 48)
font_loading_small = pygame.font.SysFont(None, 28)


def demander_pseudo(screen, clock, largeur, hauteur):
    pseudo = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pseudo = pseudo.strip()
                    if pseudo != "":
                        return pseudo
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    if event.unicode.isprintable() and len(pseudo) < 15:
                        pseudo += event.unicode

        screen.fill((15, 20, 35))

        titre = font_titre.render("Border Escape", True, (255, 255, 255))
        instruction = font_texte.render(
            "Entre ton pseudo puis appuie sur Entrée",
            True,
            (220, 220, 220)
        )

        input_rect = pygame.Rect(largeur // 2 - 180, hauteur // 2 - 20, 360, 60)
        pygame.draw.rect(screen, (40, 55, 85), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 3)

        texte_affiche = pseudo if pseudo != "" else "Pseudo..."
        couleur_texte = (255, 255, 255) if pseudo != "" else (170, 170, 170)
        texte_surface = font_input.render(texte_affiche, True, couleur_texte)

        titre_rect = titre.get_rect(center=(largeur // 2, hauteur // 2 - 140))
        instruction_rect = instruction.get_rect(center=(largeur // 2, hauteur // 2 - 70))
        texte_rect = texte_surface.get_rect(
            midleft=(input_rect.x + 15, input_rect.y + input_rect.height // 2)
        )

        screen.blit(titre, titre_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(texte_surface, texte_rect)

        pygame.display.flip()
        clock.tick(60)


def demander_mode_reseau(screen, clock, largeur, hauteur):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return "HOST"
                if event.key == pygame.K_j:
                    return "JOIN"
                if event.key == pygame.K_s:
                    return "SOLO"

        screen.fill((20, 20, 30))

        titre = font_titre.render("Choisis un mode", True, (255, 255, 255))
        ligne1 = font_texte.render("H : Host une partie", True, (220, 220, 220))
        ligne2 = font_texte.render("J : Rejoindre une partie", True, (220, 220, 220))
        ligne3 = font_texte.render("S : Solo", True, (220, 220, 220))

        screen.blit(titre, titre.get_rect(center=(largeur // 2, hauteur // 2 - 100)))
        screen.blit(ligne1, ligne1.get_rect(center=(largeur // 2, hauteur // 2 - 20)))
        screen.blit(ligne2, ligne2.get_rect(center=(largeur // 2, hauteur // 2 + 30)))
        screen.blit(ligne3, ligne3.get_rect(center=(largeur // 2, hauteur // 2 + 80)))

        pygame.display.flip()
        clock.tick(60)


def demander_ip(screen, clock, largeur, hauteur):
    ip = "127.0.0.1"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ip = ip.strip()
                    if ip != "":
                        return ip
                elif event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    if event.unicode.isprintable() and len(ip) < 30:
                        ip += event.unicode

        screen.fill((15, 20, 35))

        titre = font_titre.render("Adresse IP du serveur", True, (255, 255, 255))
        instruction = font_texte.render("Entre l'IP puis appuie sur Entrée", True, (220, 220, 220))

        input_rect = pygame.Rect(largeur // 2 - 180, hauteur // 2 - 20, 360, 60)
        pygame.draw.rect(screen, (40, 55, 85), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 3)

        texte_surface = font_input.render(ip, True, (255, 255, 255))

        titre_rect = titre.get_rect(center=(largeur // 2, hauteur // 2 - 140))
        instruction_rect = instruction.get_rect(center=(largeur // 2, hauteur // 2 - 70))
        texte_rect = texte_surface.get_rect(
            midleft=(input_rect.x + 15, input_rect.y + input_rect.height // 2)
        )

        screen.blit(titre, titre_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(texte_surface, texte_rect)

        pygame.display.flip()
        clock.tick(60)


def dessiner_loading(screen, largeur, hauteur, elapsed_ms):
    screen.fill((12, 18, 30))

    titre = font_loading.render("Chargement de la partie...", True, (255, 255, 255))
    sous_titre = font_loading_small.render("Préparation de l'exploration", True, (210, 210, 210))

    screen.blit(titre, titre.get_rect(center=(largeur // 2, hauteur // 2 - 60)))
    screen.blit(sous_titre, sous_titre.get_rect(center=(largeur // 2, hauteur // 2 - 20)))

    bar_width = 420
    bar_height = 26
    bar_x = largeur // 2 - bar_width // 2
    bar_y = hauteur // 2 + 30

    pygame.draw.rect(screen, (45, 55, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=8)

    progression = min(1.0, elapsed_ms / 1600.0)
    fill_width = int((bar_width - 6) * progression)
    pygame.draw.rect(screen, (80, 170, 120), (bar_x + 3, bar_y + 3, fill_width, bar_height - 6), border_radius=6)


def demarrer_loading():
    global etat_jeu, loading_start_time
    etat_jeu = "LOADING"
    loading_start_time = pygame.time.get_ticks()


def initialiser_partie():
    global etat_jeu, puzzle_actif, partie_terminee
    map_manager.generate_new_map()
    central_room.reset_round()
    puzzle_actif = None
    partie_terminee = False
    etat_jeu = "CENTRAL"


# -----------------------------
# Initialisation pseudo + réseau
# -----------------------------
pseudo_joueur = demander_pseudo(ecran, horloge, LARGEUR, HAUTEUR)
mode_reseau = demander_mode_reseau(ecran, horloge, LARGEUR, HAUTEUR)

server = None
client = None
est_host = mode_reseau == "HOST"

if mode_reseau == "HOST":
    server = GameServer(host="0.0.0.0", port=5000)
    server.start_server()

    client = GameClient()
    client.connect("127.0.0.1", 5000)

elif mode_reseau == "JOIN":
    ip_serveur = demander_ip(ecran, horloge, LARGEUR, HAUTEUR)
    client = GameClient()
    client.connect(ip_serveur, 5000)

# Systèmes
scoring_system = ScoringSystem()
lives_manager = LivesManager()
hud = HUD(LARGEUR)
end_screen = EndScreen(LARGEUR, HAUTEUR)
death_screen = DeathScreen(LARGEUR, HAUTEUR)
lobby_menu = LobbyMenu(LARGEUR, HAUTEUR)
lobby_menu.set_host(est_host)

# Joueur local
local_player = Player(
    pseudo_joueur,
    (52, 152, 219),
    player_id=f"{pseudo_joueur}_{pygame.time.get_ticks()}",
    is_local=True,
    x=220,
    y=360
)

# Optionnel mais utile
local_player.is_host = est_host

# Joueurs distants indexés par ID
remote_players = {}

# Chat lobby
chat_messages = []

# En solo on démarre directement, sinon on passe par le lobby
etat_jeu = "CENTRAL" if mode_reseau == "SOLO" else "LOBBY"
loading_start_time = None

# Gameplay
map_manager = MapManager()

# IMPORTANT :
# Ce main suppose que ton CentralRoom accepte maintenant un 4e paramètre optionnel client=None
central_room = CentralRoom(LARGEUR, HAUTEUR, map_manager, client)

minimap = Minimap(LARGEUR, HAUTEUR, map_manager)

puzzle_actif = None
partie_terminee = False


def update_remote_player(data):
    player_id = data["id"]

    if player_id == local_player.player_id:
        return

    if player_id not in remote_players:
        remote_players[player_id] = Player(
            nom=data.get("nom", f"Joueur_{player_id}"),
            couleur=tuple(data.get("couleur", (180, 180, 180))),
            player_id=player_id,
            is_local=False,
            x=data.get("x", 100),
            y=data.get("y", 100)
        )

    remote_players[player_id].update_from_dict(data)

    if "is_host" in data:
        remote_players[player_id].is_host = data["is_host"]


def remplacer_liste_joueurs(players_data):
    anciens_joueurs = {}

    for player_id, player in remote_players.items():
        anciens_joueurs[player_id] = {
            "x": player.x,
            "y": player.y,
            "score": player.score,
            "vies": player.vies,
            "facing_right": getattr(player, "facing_right", True),
            "is_host": getattr(player, "is_host", False)
        }

    remote_players.clear()

    for player_data in players_data:
        if player_data["id"] == local_player.player_id:
            local_player.is_host = player_data.get("is_host", local_player.is_host)
            continue

        joueur = Player(
            nom=player_data.get("nom", "Joueur"),
            couleur=tuple(player_data.get("couleur", (180, 180, 180))),
            player_id=player_data["id"],
            is_local=False,
            x=100,
            y=100
        )

        if player_data["id"] in anciens_joueurs:
            etat = anciens_joueurs[player_data["id"]]
            joueur.x = etat["x"]
            joueur.y = etat["y"]
            joueur.score = etat["score"]
            joueur.vies = etat["vies"]
            if hasattr(joueur, "facing_right"):
                joueur.facing_right = etat["facing_right"]
            joueur.is_host = etat["is_host"]

        if "x" in player_data:
            joueur.x = player_data["x"]
        if "y" in player_data:
            joueur.y = player_data["y"]
        if "score" in player_data:
            joueur.score = player_data["score"]
        if "vies" in player_data:
            joueur.vies = player_data["vies"]
        if "facing_right" in player_data and hasattr(joueur, "facing_right"):
            joueur.facing_right = player_data["facing_right"]

        joueur.is_host = player_data.get("is_host", getattr(joueur, "is_host", False))
        remote_players[player_data["id"]] = joueur


if client:
    client.send({
        "type": "JOIN",
        "id": local_player.player_id,
        "nom": local_player.nom,
        "couleur": list(local_player.couleur),
        "x": local_player.x,
        "y": local_player.y,
        "score": local_player.score,
        "vies": local_player.vies
    })

while True:
    joueur_actif = local_player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if client:
                client.disconnect()
            if server:
                server.stop()
            pygame.quit()
            sys.exit()

        # --- LOBBY ---
        if etat_jeu == "LOBBY":
            action, data = lobby_menu.handle_event(event)

            if action == "SEND_CHAT":
                if client:
                    client.send({
                        "type": "CHAT",
                        "author": local_player.nom,
                        "message": data
                    })
                else:
                    chat_messages.append(f"{local_player.nom} : {data}")
                    chat_messages = chat_messages[-30:]

            elif action == "START_GAME":
                if client:
                    client.send({"type": "START_GAME"})
                else:
                    demarrer_loading()

        # --- GESTION ÉTAT : MORT ---
        elif etat_jeu == "MORT":
            if death_screen.handle_input(event):
                joueur_actif.reset()
                map_manager.generate_new_map()
                central_room.reset_round()
                etat_jeu = "CENTRAL"

        # --- GESTION ÉTAT : ENIGME ---
        elif etat_jeu == "ENIGME" and puzzle_actif:
            resultat = puzzle_actif.handle_event(event)

            if resultat is True:
                print("Énigme réussie !")
                joueur_actif.gagner_points(100)
                map_manager.quests_completed += 1
                map_manager.check_exit_condition()
                central_room.reset_round()
                etat_jeu = "CENTRAL"
                puzzle_actif = None

            elif resultat is False:
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

    # -----------------------------
    # Réception réseau
    # -----------------------------
    if client:
        messages = client.get_messages()

        for message in messages:
            msg_type = message.get("type")

            if msg_type == "PLAYER_LIST":
                remplacer_liste_joueurs(message.get("players", []))

                # Met à jour le host côté local si l'info arrive
                for pdata in message.get("players", []):
                    if pdata.get("id") == local_player.player_id:
                        local_player.is_host = pdata.get("is_host", local_player.is_host)
                        lobby_menu.set_host(local_player.is_host)
                        break

                if message.get("game_started", False) and etat_jeu == "LOBBY":
                    demarrer_loading()

            elif msg_type == "START_GAME":
                if etat_jeu == "LOBBY":
                    demarrer_loading()

            elif msg_type == "PLAYER_STATE":
                update_remote_player(message)

            elif msg_type == "CHAT":
                auteur = message.get("author", "Inconnu")
                texte = message.get("message", "")
                chat_messages.append(f"{auteur} : {texte}")
                chat_messages = chat_messages[-30:]

            elif msg_type == "DICE_RESULT":
                # IMPORTANT :
                # suppose que CentralRoom possède apply_dice_result(message)
                central_room.apply_dice_result(message)

            elif msg_type == "MOVE":
                # Avec ton MapManager actuel, on ne déplace que la position logique du joueur local
                if message.get("id") == local_player.player_id:
                    map_manager.move_player(message.get("dir"))

    # Déplacement dans le lobby (si ton ui/menu.py possède update())
    if etat_jeu == "LOBBY":
        if hasattr(lobby_menu, "update"):
            lobby_menu.update()

    # État de chargement
    elif etat_jeu == "LOADING":
        now = pygame.time.get_ticks()
        if loading_start_time is None:
            loading_start_time = now

        if now - loading_start_time >= 1600:
            initialiser_partie()

    # Déplacement uniquement du joueur local
    elif etat_jeu == "CENTRAL" and not partie_terminee:
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            local_player.x -= local_player.speed
            if hasattr(local_player, "facing_right"):
                local_player.facing_right = False

        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            local_player.x += local_player.speed
            if hasattr(local_player, "facing_right"):
                local_player.facing_right = True

        if touches[pygame.K_UP] or touches[pygame.K_z]:
            local_player.y -= local_player.speed

        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            local_player.y += local_player.speed

        local_player.x = max(0, min(LARGEUR - local_player.width, local_player.x))
        local_player.y = max(0, min(HAUTEUR - local_player.height, local_player.y))

    # -----------------------------
    # Envoi état local
    # -----------------------------
    if client and etat_jeu in ("LOBBY", "CENTRAL"):
        payload = {
            "type": "PLAYER_STATE",
            "id": local_player.player_id,
            "nom": local_player.nom,
            "x": local_player.x,
            "y": local_player.y,
            "score": local_player.score,
            "vies": local_player.vies,
            "couleur": list(local_player.couleur),
            "is_host": getattr(local_player, "is_host", est_host)
        }

        if hasattr(local_player, "facing_right"):
            payload["facing_right"] = local_player.facing_right

        client.send(payload)

    joueurs = [local_player] + list(remote_players.values())

    # Synchronisation affichage lobby
    lobby_menu.update_players(joueurs)
    lobby_menu.set_chat_messages(chat_messages)

    # --- UPDATE & DRAW ---
    if etat_jeu == "LOBBY":
        lobby_menu.draw(ecran)

    elif etat_jeu == "LOADING":
        elapsed = pygame.time.get_ticks() - loading_start_time if loading_start_time else 0
        dessiner_loading(ecran, LARGEUR, HAUTEUR, elapsed)

    elif not partie_terminee:
        ecran.fill((0, 0, 0))

        if etat_jeu == "CENTRAL":
            result = central_room.update(local_player, len(joueurs))
            central_room.draw(ecran)

            local_player.draw(ecran, font_joueur, actif=True)

            for joueur in remote_players.values():
                joueur.draw(ecran, font_joueur, actif=False)

            if local_player.vies <= 0:
                etat_jeu = "MORT"

            elif result == "LANCER_ENIGME":
                puzzle_actif = PuzzleRoom()
                etat_jeu = "ENIGME"

            elif result == "FIN_DU_JEU":
                partie_terminee = True

        elif etat_jeu == "ENIGME" and puzzle_actif:
            puzzle_actif.draw(ecran)

        elif etat_jeu == "MORT":
            central_room.draw(ecran)

            local_player.draw(ecran, font_joueur, actif=True)
            for joueur in remote_players.values():
                joueur.draw(ecran, font_joueur, actif=False)

            death_screen.draw(ecran)

        if etat_jeu != "MORT":
            scoring_system.afficher_hud_score(ecran, joueurs, 0, map_manager)
            lives_manager.afficher_vies(ecran, local_player)
            minimap.draw(ecran)

    else:
        end_screen.afficher(ecran, joueurs)

    pygame.display.flip()
    horloge.tick(60)