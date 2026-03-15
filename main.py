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
font_lobby = pygame.font.SysFont(None, 32)
font_chat = pygame.font.SysFont(None, 26)


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


def dessiner_lobby(screen, largeur, hauteur, players, est_host, chat_messages, chat_input):
    screen.fill((18, 24, 40))

    titre = font_titre.render("Lobby Multijoueur", True, (255, 255, 255))
    sous_titre = font_texte.render("Joueurs connectés :", True, (220, 220, 220))

    screen.blit(titre, titre.get_rect(center=(largeur // 2, 60)))
    screen.blit(sous_titre, sous_titre.get_rect(center=(220, 130)))

    y = 180
    for player in players:
        texte = font_lobby.render(f"- {player.nom}", True, player.couleur)
        screen.blit(texte, (80, y))
        y += 40

    chat_box = pygame.Rect(450, 140, 480, 360)
    pygame.draw.rect(screen, (30, 38, 58), chat_box)
    pygame.draw.rect(screen, (255, 255, 255), chat_box, 2)

    chat_title = font_texte.render("Chat", True, (255, 255, 255))
    screen.blit(chat_title, (460, 105))

    visible_messages = chat_messages[-10:]
    y_msg = 160
    for msg in visible_messages:
        texte = font_chat.render(msg, True, (235, 235, 235))
        screen.blit(texte, (465, y_msg))
        y_msg += 30

    input_box = pygame.Rect(450, 530, 480, 50)
    pygame.draw.rect(screen, (40, 55, 85), input_box)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

    prefix = font_chat.render("> ", True, (255, 255, 255))
    input_surface = font_chat.render(
        chat_input if chat_input else "Écris un message...",
        True,
        (255, 255, 255) if chat_input else (160, 160, 160)
    )
    screen.blit(prefix, (462, 542))
    screen.blit(input_surface, (485, 542))

    if est_host:
        info = font_texte.render("Espace : lancer la partie", True, (255, 255, 255))
    else:
        info = font_texte.render("En attente du lancement par l'host...", True, (200, 200, 200))

    screen.blit(info, info.get_rect(center=(largeur // 2, hauteur - 40)))


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

# Joueur local
local_player = Player(
    pseudo_joueur,
    (52, 152, 219),
    player_id=f"{pseudo_joueur}_{pygame.time.get_ticks()}",
    is_local=True,
    x=220,
    y=360
)

# Joueurs distants indexés par ID
remote_players = {}

# Chat lobby
chat_messages = []
chat_input = ""

# En solo on démarre directement, sinon on passe par le lobby
etat_jeu = "CENTRAL" if mode_reseau == "SOLO" else "LOBBY"


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


def remplacer_liste_joueurs(players_data):
    anciens_joueurs = {}

    for player_id, player in remote_players.items():
        anciens_joueurs[player_id] = {
            "x": player.x,
            "y": player.y,
            "score": player.score,
            "vies": player.vies
        }

    remote_players.clear()

    for player_data in players_data:
        if player_data["id"] == local_player.player_id:
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

        remote_players[player_data["id"]] = joueur


if client:
    client.send({
        "type": "JOIN",
        "id": local_player.player_id,
        "nom": local_player.nom,
        "couleur": list(local_player.couleur)
    })

# Gameplay
map_manager = MapManager()
central_room = CentralRoom(LARGEUR, HAUTEUR, map_manager)
minimap = Minimap(LARGEUR, HAUTEUR, map_manager)

puzzle_actif = None
partie_terminee = False

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    message = chat_input.strip()
                    if message and client:
                        client.send({
                            "type": "CHAT",
                            "author": local_player.nom,
                            "message": message
                        })
                    chat_input = ""

                elif est_host and event.key == pygame.K_SPACE:
                    if client:
                        client.send({"type": "START_GAME"})
                    etat_jeu = "CENTRAL"

                elif event.key == pygame.K_BACKSPACE:
                    chat_input = chat_input[:-1]

                else:
                    if event.unicode.isprintable() and len(chat_input) < 60:
                        chat_input += event.unicode

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

            elif msg_type == "START_GAME":
                etat_jeu = "CENTRAL"

            elif msg_type == "PLAYER_STATE":
                update_remote_player(message)

            elif msg_type == "CHAT":
                auteur = message.get("author", "Inconnu")
                texte = message.get("message", "")
                chat_messages.append(f"{auteur} : {texte}")
                chat_messages = chat_messages[-30:]

    # Déplacement uniquement du joueur local
    if etat_jeu == "CENTRAL" and not partie_terminee:
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            local_player.x -= local_player.speed
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            local_player.x += local_player.speed
        if touches[pygame.K_UP] or touches[pygame.K_z]:
            local_player.y -= local_player.speed
        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            local_player.y += local_player.speed

        local_player.x = max(0, min(LARGEUR - local_player.width, local_player.x))
        local_player.y = max(0, min(HAUTEUR - local_player.height, local_player.y))

    # -----------------------------
    # Envoi état local
    # -----------------------------
    if client and etat_jeu == "CENTRAL":
        client.send({
            "type": "PLAYER_STATE",
            "id": local_player.player_id,
            "nom": local_player.nom,
            "x": local_player.x,
            "y": local_player.y,
            "score": local_player.score,
            "vies": local_player.vies,
            "couleur": list(local_player.couleur)
        })

    joueurs = [local_player] + list(remote_players.values())

    # --- UPDATE & DRAW ---
    if etat_jeu == "LOBBY":
        dessiner_lobby(
            ecran,
            LARGEUR,
            HAUTEUR,
            joueurs,
            est_host,
            chat_messages,
            chat_input
        )

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