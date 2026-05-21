import pygame
import sys

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
from world.world_manager import WorldManager # NOUVEAU : Import du monde

print("MAIN VERSION CORRIGEE")
print(__file__)

pygame.init()
LARGEUR, HAUTEUR = 1000, 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Border Escape - Full Game")
horloge = pygame.time.Clock()

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


# NOUVEAU : Fonction pour choisir le personnage
def demander_personnage(screen, clock, largeur, hauteur):
    persos = ["assets/perso1.png", "assets/perso2.png", "assets/perso3.png"]
    images = []
    for p in persos:
        try:
            img = pygame.image.load(p).convert_alpha()
            images.append(pygame.transform.scale(img, (100, 100)))
        except:
            surf = pygame.Surface((500, 500))
            surf.fill((255, 0, 255))
            images.append(surf)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(3):
                    rect = pygame.Rect(largeur // 2 - 200 + i * 150, hauteur // 2, 100, 100)
                    if rect.collidepoint((mx, my)):
                        return persos[i]

        screen.fill((15, 20, 35))
        titre = font_titre.render("Choisis ton personnage", True, (255, 255, 255))
        screen.blit(titre, titre.get_rect(center=(largeur // 2, hauteur // 2 - 100)))

        for i, img in enumerate(images):
            screen.blit(img, (largeur // 2 - 200 + i * 150, hauteur // 2))

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


def build_map_data():
    return {
        "grid": [row[:] for row in map_manager.grid],
        "player_pos": map_manager.player_pos[:],
        "exit_pos": map_manager.exit_pos[:],
        "quests_completed": map_manager.quests_completed,
        "min_quests_to_exit": map_manager.min_quests_to_exit,
        "exit_revealed": map_manager.exit_revealed
    }


def demarrer_loading():
    global etat_jeu, loading_start_time
    etat_jeu = "LOADING"
    loading_start_time = pygame.time.get_ticks()


def initialiser_partie():
    global etat_jeu, puzzle_actif, partie_terminee, map_loaded

    if mode_reseau == "SOLO":
        map_manager.generate_new_map()
        map_loaded = True

    elif est_host and not map_loaded:
        map_manager.generate_new_map()
        map_loaded = True

        if client:
            client.send({
                "type": "MAP_DATA",
                "map_data": build_map_data()
            })

    if map_loaded:
        central_room.reset_round()
        puzzle_actif = None
        partie_terminee = False
        etat_jeu = "CENTRAL"


def meme_salle(room_a, room_b):
    return list(room_a) == list(room_b)


def get_joueurs_meme_salle():
    salle_locale = map_manager.player_pos[:]
    joueurs_meme_salle = [local_player]

    for joueur in remote_players.values():
        room_pos = getattr(joueur, "room_pos", None)
        if room_pos is not None and meme_salle(room_pos, salle_locale):
            joueurs_meme_salle.append(joueur)

    return joueurs_meme_salle


def draw_remote_players_same_room(screen, font):
    salle_locale = map_manager.player_pos[:]

    for joueur in remote_players.values():
        room_pos = getattr(joueur, "room_pos", None)
        if room_pos is None:
            continue
        if not meme_salle(room_pos, salle_locale):
            continue
        joueur.draw(screen, font, actif=False)


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
            y=data.get("y", 100),
            image_path=data.get("image_path") # NOUVEAU
        )

    joueur = remote_players[player_id]
    joueur.update_from_dict(data)
    joueur.is_host = data.get("is_host", False)
    joueur.room_pos = data.get("room_pos", [1, 1])


def remplacer_liste_joueurs(players_data):
    anciens = {}
    for pid, p in remote_players.items():
        anciens[pid] = {
            "x": p.x,
            "y": p.y,
            "score": p.score,
            "vies": p.vies,
            "facing_right": getattr(p, "facing_right", True),
            "is_host": getattr(p, "is_host", False),
            "room_pos": getattr(p, "room_pos", [1, 1]),
            "image_path": getattr(p, "image_path", None) # NOUVEAU
        }

    remote_players.clear()

    for pdata in players_data:
        if pdata["id"] == local_player.player_id:
            local_player.is_host = est_host or pdata.get("is_host", False)
            continue

        joueur = Player(
            nom=pdata.get("nom", "Joueur"),
            couleur=tuple(pdata.get("couleur", (180, 180, 180))),
            player_id=pdata["id"],
            is_local=False,
            x=pdata.get("x", 100),
            y=pdata.get("y", 100),
            image_path=pdata.get("image_path") # NOUVEAU
        )

        if pdata["id"] in anciens:
            old = anciens[pdata["id"]]
            joueur.x = old["x"]
            joueur.y = old["y"]
            joueur.score = old["score"]
            joueur.vies = old["vies"]
            joueur.facing_right = old["facing_right"]
            joueur.is_host = old["is_host"]
            joueur.room_pos = old["room_pos"]

        joueur.x = pdata.get("x", joueur.x)
        joueur.y = pdata.get("y", joueur.y)
        joueur.score = pdata.get("score", joueur.score)
        joueur.vies = pdata.get("vies", joueur.vies)
        joueur.facing_right = pdata.get("facing_right", joueur.facing_right)
        joueur.is_host = pdata.get("is_host", joueur.is_host)
        joueur.room_pos = pdata.get("room_pos", getattr(joueur, "room_pos", [1, 1]))

        remote_players[pdata["id"]] = joueur


def deplacer_joueur_dans_lobby():
    touches = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if touches[pygame.K_LEFT]:
        dx -= local_player.speed
    if touches[pygame.K_RIGHT]:
        dx += local_player.speed
    if touches[pygame.K_UP]:
        dy -= local_player.speed
    if touches[pygame.K_DOWN]:
        dy += local_player.speed

    if dx != 0 or dy != 0:
        local_player.move(
            dx,
            dy,
            min_x=30,
            max_x=LARGEUR - 30,
            min_y=110,
            max_y=HAUTEUR - 170
        )


pseudo_joueur = demander_pseudo(ecran, horloge, LARGEUR, HAUTEUR)
image_perso = demander_personnage(ecran, horloge, LARGEUR, HAUTEUR) # NOUVEAU
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

scoring_system = ScoringSystem()
lives_manager = LivesManager()
hud = HUD(LARGEUR)
end_screen = EndScreen(LARGEUR, HAUTEUR)
death_screen = DeathScreen(LARGEUR, HAUTEUR)
lobby_menu = LobbyMenu(LARGEUR, HAUTEUR)

# NOUVEAU : On génère le sol du monde !
world_manager = WorldManager()
world_manager.generate_world()

local_player = Player(
    pseudo_joueur,
    (52, 152, 219),
    player_id=f"{pseudo_joueur}_{pygame.time.get_ticks()}",
    is_local=True,
    x=220,
    y=360,
    image_path=image_perso # NOUVEAU : Application de l'image
)
local_player.is_host = est_host

lobby_menu.set_host(est_host)
lobby_menu.set_local_player_id(local_player.player_id)

remote_players = {}
chat_messages = []

etat_jeu = "CENTRAL" if mode_reseau == "SOLO" else "LOBBY"
loading_start_time = None
map_loaded = mode_reseau == "SOLO"

map_manager = MapManager()
central_room = CentralRoom(LARGEUR, HAUTEUR, map_manager, client)
minimap = Minimap(LARGEUR, HAUTEUR, map_manager)

puzzle_actif = None
partie_terminee = False

if client:
    client.send({
        "type": "JOIN",
        "id": local_player.player_id,
        "nom": local_player.nom,
        "couleur": list(local_player.couleur),
        "x": local_player.x,
        "y": local_player.y,
        "score": local_player.score,
        "vies": local_player.vies,
        "facing_right": local_player.facing_right,
        "room_pos": map_manager.player_pos[:],
        "image_path": local_player.image_path # NOUVEAU
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

        elif etat_jeu == "MORT":
            if death_screen.handle_input(event):
                joueur_actif.reset()
                map_manager.generate_new_map()
                central_room.reset_round()
                etat_jeu = "CENTRAL"

        elif etat_jeu == "ENIGME" and puzzle_actif:
            resultat = puzzle_actif.handle_event(event)

            if resultat is True:
                joueur_actif.gagner_points(100)
                map_manager.quests_completed += 1
                map_manager.check_exit_condition()
                central_room.reset_round()
                etat_jeu = "CENTRAL"
                puzzle_actif = None

            elif resultat is False:
                joueur_actif.perdre_points(50)
                joueur_actif.perdre_vie()

                if joueur_actif.vies <= 0:
                    etat_jeu = "MORT"
                else:
                    puzzle_actif = PuzzleRoom()

        elif etat_jeu == "CENTRAL":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    minimap.toggle()

    if client:
        messages = client.get_messages()

        for message in messages:
            msg_type = message.get("type")

            if msg_type == "PLAYER_LIST":
                remplacer_liste_joueurs(message.get("players", []))
                lobby_menu.set_host(local_player.is_host)

                if message.get("game_started", False) and etat_jeu == "LOBBY":
                    demarrer_loading()

            elif msg_type == "START_GAME":
                if etat_jeu == "LOBBY":
                    demarrer_loading()

            elif msg_type == "MAP_DATA":
                data = message["map_data"]

                map_manager.grid = [row[:] for row in data["grid"]]
                map_manager.player_pos = list(data.get("player_pos", [1, 1]))
                map_manager.exit_pos = list(data.get("exit_pos", [0, 0]))
                map_manager.quests_completed = data.get("quests_completed", 0)
                map_manager.min_quests_to_exit = data.get("min_quests_to_exit", 2)
                map_manager.exit_revealed = data.get("exit_revealed", False)

                map_loaded = True

                if etat_jeu == "LOADING":
                    initialiser_partie()

            elif msg_type == "PLAYER_STATE":
                update_remote_player(message)

            elif msg_type == "CHAT":
                auteur = message.get("author", "Inconnu")
                texte = message.get("message", "")
                chat_messages.append(f"{auteur} : {texte}")
                chat_messages = chat_messages[-30:]

            elif msg_type == "DICE_RESULT":
                central_room.apply_dice_result(message)

    joueurs = [local_player] + list(remote_players.values())
    joueurs_meme_salle = get_joueurs_meme_salle()

    lobby_menu.update_players(joueurs)
    lobby_menu.set_chat_messages(chat_messages)

    if etat_jeu == "LOBBY":
        deplacer_joueur_dans_lobby()
        lobby_menu.update()

    elif etat_jeu == "LOADING":
        now = pygame.time.get_ticks()
        if loading_start_time is None:
            loading_start_time = now

        if now - loading_start_time >= 1600:
            initialiser_partie()

    elif etat_jeu == "CENTRAL" and not partie_terminee:
        touches = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            dx -= local_player.speed
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            dx += local_player.speed
        if touches[pygame.K_UP] or touches[pygame.K_z]:
            dy -= local_player.speed
        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            dy += local_player.speed

        local_player.move(
            dx,
            dy,
            min_x=0,
            max_x=LARGEUR,
            min_y=0,
            max_y=HAUTEUR
        )

        result = central_room.update(
            local_player,
            len(joueurs_meme_salle),
            can_roll_dice=(mode_reseau == "SOLO" or est_host)
        )

        if local_player.vies <= 0:
            etat_jeu = "MORT"

        elif result == "LANCER_ENIGME":
            puzzle_actif = PuzzleRoom()
            etat_jeu = "ENIGME"

        elif result == "FIN_DU_JEU":
            partie_terminee = True

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
            "is_host": est_host,
            "facing_right": getattr(local_player, "facing_right", True),
            "room_pos": map_manager.player_pos[:],
            "image_path": getattr(local_player, "image_path", None) # NOUVEAU
        }
        client.send(payload)

    if etat_jeu == "LOBBY":
        lobby_menu.draw(ecran)

    elif etat_jeu == "LOADING":
        elapsed = pygame.time.get_ticks() - loading_start_time if loading_start_time else 0
        dessiner_loading(ecran, LARGEUR, HAUTEUR, elapsed)

    elif not partie_terminee:
        # NOUVEAU : On dessine le sol de la grotte !
        world_manager.draw(ecran)

        if etat_jeu == "CENTRAL":
            central_room.draw(ecran)

            local_player.draw(ecran, font_joueur, actif=True)
            draw_remote_players_same_room(ecran, font_joueur)

        elif etat_jeu == "ENIGME" and puzzle_actif:
            puzzle_actif.draw(ecran)

        elif etat_jeu == "MORT":
            central_room.draw(ecran)
            local_player.draw(ecran, font_joueur, actif=True)
            draw_remote_players_same_room(ecran, font_joueur)
            death_screen.draw(ecran)

        if etat_jeu != "MORT":
            scoring_system.afficher_hud_score(ecran, joueurs, 0, map_manager)
            lives_manager.afficher_vies(ecran, local_player)
            minimap.draw(ecran)

    else:
        end_screen.afficher(ecran, joueurs)

    pygame.display.flip()
    horloge.tick(60)