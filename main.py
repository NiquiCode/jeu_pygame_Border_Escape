import pygame
import sys
import os
import random

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
from ui.main_menu import MainMenu
from ui.options_menu import OptionsMenu
from network.server import GameServer
from network.client import GameClient
from gameplay.npc_master import NPCMaster
from ui.dice import Dice 

pygame.init()
pygame.mixer.init()

LARGEUR, HAUTEUR = 1000, 700
flags = pygame.RESIZABLE | pygame.SCALED
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), flags)
is_fullscreen = False
pygame.display.set_caption("Border Escape - Full Game")
horloge = pygame.time.Clock()

font_joueur = pygame.font.SysFont(None, 24)
font_titre = pygame.font.SysFont(None, 52)
font_texte = pygame.font.SysFont(None, 36)
font_input = pygame.font.SysFont(None, 42)
font_loading = pygame.font.SysFont(None, 48)

sons = {}
try:
    sons["intro"] = pygame.mixer.Sound("assets/intro_theme.mp3")
    sons["game"] = pygame.mixer.Sound("assets/gameplay_loop.mp3")
    sons["win_salle"] = pygame.mixer.Sound("assets/win_enigma.wav")
    sons["lose_salle"] = pygame.mixer.Sound("assets/lose_enigma.wav")
    sons["win_game"] = pygame.mixer.Sound("assets/game_won.mp3")
    sons["lose_game"] = pygame.mixer.Sound("assets/game_over.mp3")
    sons["intro"].play(loops=-1)
    sons["intro"].set_volume(0.5)
except:
    pass

sorcier = NPCMaster(LARGEUR, HAUTEUR)
de_jeu = Dice(LARGEUR // 2, HAUTEUR // 2 - 110) 

menu_principal = MainMenu(LARGEUR, HAUTEUR)
options_menu = OptionsMenu(LARGEUR, HAUTEUR, sons)

def check_global_events():
    global is_fullscreen, ecran
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN | pygame.SCALED)
            else:
                ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE | pygame.SCALED)
        yield event

def demander_pseudo(screen, clock, largeur, hauteur):
    pseudo = ""
    try:
        bg = pygame.image.load("assets/menu_bg.png").convert()
        bg = pygame.transform.scale(bg, (largeur, hauteur))
    except:
        bg = pygame.Surface((largeur, hauteur)); bg.fill((15, 20, 35))
    overlay = pygame.Surface((largeur, hauteur), pygame.SRCALPHA); overlay.fill((0, 0, 0, 190)) 
    
    while True:
        for event in check_global_events():
            if event.type == pygame.KEYDOWN and event.key != pygame.K_F11:
                if event.key == pygame.K_RETURN and pseudo.strip(): return pseudo.strip()
                elif event.key == pygame.K_BACKSPACE: pseudo = pseudo[:-1]
                elif event.unicode.isprintable() and len(pseudo) < 15: pseudo += event.unicode

        screen.blit(bg, (0, 0)); screen.blit(overlay, (0, 0))
        titre = font_titre.render("IDENTIFICATION", True, (0, 255, 255))
        instruction = font_texte.render("Entre ton pseudo :", True, (200, 200, 200))
        input_rect = pygame.Rect(largeur // 2 - 180, hauteur // 2 - 20, 360, 60)
        pygame.draw.rect(screen, (10, 15, 25), input_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 255, 255), input_rect, 2, border_radius=8)
        
        texte_affiche = pseudo if pseudo != "" else "Taper ici..."
        couleur_texte = (255, 255, 255) if pseudo != "" else (100, 100, 100)
        texte_surface = font_input.render(texte_affiche, True, couleur_texte)
        
        screen.blit(titre, titre.get_rect(center=(largeur // 2, hauteur // 2 - 120)))
        screen.blit(instruction, instruction.get_rect(center=(largeur // 2, hauteur // 2 - 60)))
        screen.blit(texte_surface, texte_surface.get_rect(midleft=(input_rect.x + 20, input_rect.y + input_rect.height // 2)))
        pygame.display.flip(); clock.tick(60)

def demander_personnage(screen, clock, largeur, hauteur):
    skins = ["assets/perso1.png", "assets/perso2.png", "assets/perso3.png", "assets/perso4.png"]
    images = []
    for s in skins:
        try:
            img = pygame.image.load(s).convert_alpha()
            img = pygame.transform.scale(img, (80, 80))
            images.append(img)
        except:
            surf = pygame.Surface((80, 80)); surf.fill((100, 100, 100)); images.append(surf)

    try:
        bg = pygame.image.load("assets/menu_bg.png").convert()
        bg = pygame.transform.scale(bg, (largeur, hauteur))
    except:
        bg = pygame.Surface((largeur, hauteur)); bg.fill((15, 20, 35))
    overlay = pygame.Surface((largeur, hauteur), pygame.SRCALPHA); overlay.fill((0, 0, 0, 190))

    boxes = [
        pygame.Rect(largeur//2 - 250, hauteur//2 - 70, 120, 120),
        pygame.Rect(largeur//2 - 100, hauteur//2 - 70, 120, 120),
        pygame.Rect(largeur//2 + 50, hauteur//2 - 70, 120, 120),
        pygame.Rect(largeur//2 + 200, hauteur//2 - 70, 120, 120)
    ]

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in check_global_events():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, box in enumerate(boxes):
                    if box.collidepoint(event.pos): return skins[idx]

        screen.blit(bg, (0, 0)); screen.blit(overlay, (0, 0))
        titre = font_titre.render("CHOIX DU SKIN", True, (0, 255, 255))
        screen.blit(titre, titre.get_rect(center=(largeur // 2, 100)))
        
        for idx, box in enumerate(boxes):
            hovered = box.collidepoint(mx, my)
            box_color = (30, 144, 255) if hovered else (30, 40, 60)
            pygame.draw.rect(screen, box_color, box, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255) if hovered else (100, 100, 100), box, 3, border_radius=12)
            img_rect = images[idx].get_rect(center=box.center)
            screen.blit(images[idx], img_rect)

        pygame.display.flip(); clock.tick(60)

def demander_mode_reseau(screen, clock, largeur, hauteur):
    try:
        bg = pygame.image.load("assets/menu_bg.png").convert()
        bg = pygame.transform.scale(bg, (largeur, hauteur))
    except:
        bg = pygame.Surface((largeur, hauteur)); bg.fill((15, 20, 35))
    overlay = pygame.Surface((largeur, hauteur), pygame.SRCALPHA); overlay.fill((0, 0, 0, 190))
    while True:
        for event in check_global_events():
            if event.type == pygame.KEYDOWN and event.key != pygame.K_F11:
                if event.key == pygame.K_h: return "HOST"
                if event.key == pygame.K_j: return "JOIN"
                if event.key == pygame.K_s: return "SOLO"
        screen.blit(bg, (0, 0)); screen.blit(overlay, (0, 0))
        txt = font_texte.render("H: Host | J: Join | S: Solo", True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=(largeur // 2, hauteur // 2)))
        pygame.display.flip(); clock.tick(60)

def demander_ip(screen, clock, largeur, hauteur):
    ip = "127.0.0.1"
    while True:
        for event in check_global_events():
            if event.type == pygame.KEYDOWN and event.key != pygame.K_F11:
                if event.key == pygame.K_RETURN: return ip.strip() if ip.strip() else "127.0.0.1"
                elif event.key == pygame.K_BACKSPACE: ip = ip[:-1]
                else:
                    if event.unicode.isprintable() and len(ip) < 30: ip += event.unicode
        screen.fill((15, 20, 35))
        titre = font_titre.render("IP du serveur", True, (255, 255, 255))
        input_rect = pygame.Rect(largeur // 2 - 180, hauteur // 2 - 20, 360, 60)
        pygame.draw.rect(screen, (40, 55, 85), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 3)
        texte_surface = font_input.render(ip, True, (255, 255, 255))
        screen.blit(titre, titre.get_rect(center=(largeur // 2, hauteur // 2 - 140)))
        screen.blit(texte_surface, texte_surface.get_rect(midleft=(input_rect.x + 15, input_rect.y + input_rect.height // 2)))
        pygame.display.flip(); clock.tick(60)

def dessiner_loading(screen, l, h, t):
    screen.fill((0, 0, 0))
    txt = font_loading.render(f"Chargement... {min(100, int(t / 16))}%", True, (255, 255, 255))
    screen.blit(txt, (l // 2 - txt.get_width() // 2, h // 2))
    pygame.display.flip()

def get_objectives_for_players(num_players):
    scaling = {1: 5, 2: 8, 3: 12, 4: 16, 5: 18, 6: 20, 7: 22, 8: 25}
    return scaling.get(num_players, 25)

def build_map_data():
    return {
        "grid": [row[:] for row in map_manager.grid], "player_pos": map_manager.player_pos[:],
        "exit_pos": map_manager.exit_pos[:], "quests_completed": map_manager.quests_completed,
        "min_quests_to_exit": map_manager.min_quests_to_exit, "exit_revealed": map_manager.exit_revealed
    }

def demarrer_loading():
    global etat_jeu, loading_start_time
    etat_jeu = "LOADING"
    loading_start_time = pygame.time.get_ticks()

def initialiser_partie():
    global etat_jeu, puzzle_actif, partie_terminee, map_loaded, current_roller_id
    if mode_reseau == "SOLO":
        map_manager.generate_new_map()
        map_loaded = True
        map_manager.min_quests_to_exit = get_objectives_for_players(1)
        current_roller_id = local_player.player_id
    elif est_host and not map_loaded:
        map_manager.generate_new_map()
        map_loaded = True
        nb_joueurs = 1 + len(remote_players)
        map_manager.min_quests_to_exit = get_objectives_for_players(nb_joueurs)
        joueurs_vivants = [p for p in [local_player] + list(remote_players.values()) if p.vies > 0]
        if joueurs_vivants:
            current_roller_id = random.choice(joueurs_vivants).player_id
            if client:
                client.send({"type": "MAP_DATA", "map_data": build_map_data()})
                client.send({"type": "NEW_ROLLER", "roller_id": current_roller_id})
    
    if map_loaded:
        central_room.reset_round()
        puzzle_actif = None
        partie_terminee = False
        etat_jeu = "CENTRAL"

def meme_salle(room_a, room_b): return list(room_a) == list(room_b)

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
        if room_pos is not None and meme_salle(room_pos, salle_locale):
            joueur.draw(screen, font, actif=False)
            if getattr(joueur, 'est_bloque', False):
                pygame.draw.rect(screen, (255, 0, 0), (joueur.x + joueur.size//2 - 10, joueur.y - 20, 20, 15), border_radius=4)
                pygame.draw.circle(screen, (255, 0, 0), (joueur.x + joueur.size//2, joueur.y - 20), 8, 3)

def update_remote_player(data):
    player_id = data["id"]
    if player_id == local_player.player_id: return
    if player_id not in remote_players:
        remote_players[player_id] = Player(
            nom=data.get("nom", f"Joueur_{player_id}"), couleur=tuple(data.get("couleur", (180, 180, 180))),
            player_id=player_id, is_local=False, x=data.get("x", 100), y=data.get("y", 100), image_path=data.get("image_path")
        )
    joueur = remote_players[player_id]
    joueur.update_from_dict(data)
    if "image_path" in data and data["image_path"]:
        if joueur.image_path != data["image_path"]:
            joueur.image_path = data["image_path"]
            joueur.charger_image()

def remplacer_liste_joueurs(players_data):
    anciens = {pid: {"x": p.x, "y": p.y, "score": p.score, "vies": p.vies, "indices_restants": getattr(p, "indices_restants", 3), "est_bloque": getattr(p, "est_bloque", False), "room_pos": getattr(p, "room_pos", [1, 1]), "image_path": getattr(p, "image_path", None)} for pid, p in remote_players.items()}
    remote_players.clear()
    for pdata in players_data:
        if pdata["id"] == local_player.player_id: continue
        img_path = pdata.get("image_path")
        if not img_path and pdata["id"] in anciens: img_path = anciens[pdata["id"]]["image_path"]
        joueur = Player(nom=pdata.get("nom", "Joueur"), couleur=tuple(pdata.get("couleur", (180, 180, 180))), player_id=pdata["id"], is_local=False, x=pdata.get("x", 100), y=pdata.get("y", 100), image_path=img_path)
        if pdata["id"] in anciens:
            old = anciens[pdata["id"]]
            joueur.x, joueur.y, joueur.score, joueur.vies, joueur.indices_restants, joueur.est_bloque, joueur.room_pos = old["x"], old["y"], old["score"], old["vies"], old["indices_restants"], old["est_bloque"], old["room_pos"]
        remote_players[pdata["id"]] = joueur


# ================== BOUCLE GLOBALE ==================
while True:
    while True:
        choix = menu_principal.afficher(ecran, horloge)
        if choix == "JOUER": break
        elif choix == "OPTIONS": options_menu.afficher(ecran, horloge)
        elif choix == "QUITTER": pygame.quit(); sys.exit()

    pseudo_joueur = demander_pseudo(ecran, horloge, LARGEUR, HAUTEUR)
    image_perso = demander_personnage(ecran, horloge, LARGEUR, HAUTEUR)
    mode_reseau = demander_mode_reseau(ecran, horloge, LARGEUR, HAUTEUR)

    server = None
    client = None
    est_host = mode_reseau == "HOST"

    if mode_reseau == "HOST":
        server = GameServer(host="0.0.0.0", port=5000); server.start_server()
        client = GameClient(); client.connect("127.0.0.1", 5000)
    elif mode_reseau == "JOIN":
        ip_serveur = demander_ip(ecran, horloge, LARGEUR, HAUTEUR)
        client = GameClient(); client.connect(ip_serveur, 5000)

    local_player = Player(pseudo_joueur, (52, 152, 219), player_id=f"{pseudo_joueur}_{pygame.time.get_ticks()}", is_local=True, x=220, y=360, image_path=image_perso)
    local_player.is_host = est_host

    current_roller_id = local_player.player_id
    is_my_turn = True
    roller_name = local_player.nom

    lobby_menu = LobbyMenu(LARGEUR, HAUTEUR)
    lobby_menu.set_host(est_host)
    lobby_menu.set_local_player_id(local_player.player_id)

    scoring_system = ScoringSystem()
    lives_manager = LivesManager()
    hud = HUD(LARGEUR, HAUTEUR)
    end_screen = EndScreen(LARGEUR, HAUTEUR)
    death_screen = DeathScreen(LARGEUR, HAUTEUR)

    remote_players = {}
    chat_messages = []
    etat_jeu = "CENTRAL" if mode_reseau == "SOLO" else "LOBBY"
    loading_start_time = None
    map_loaded = mode_reseau == "SOLO"
    spectator_index = 0

    map_manager = MapManager()
    central_room = CentralRoom(LARGEUR, HAUTEUR, map_manager, client)
    minimap = Minimap(LARGEUR, HAUTEUR, map_manager)

    puzzle_actif = None
    partie_terminee = False

    if client:
        client.send({
            "type": "JOIN", "id": local_player.player_id, "nom": local_player.nom,
            "couleur": list(local_player.couleur), "x": local_player.x, "y": local_player.y,
            "score": local_player.score, "vies": local_player.vies, "indices_restants": local_player.indices_restants, "facing_right": local_player.facing_right,
            "room_pos": map_manager.player_pos[:], "image_path": local_player.image_path
        })

    while True:
        joueur_actif = local_player
        touches = pygame.key.get_pressed()
        joueurs = [local_player] + list(remote_players.values())
        joueurs_meme_salle = get_joueurs_meme_salle()

        is_my_turn = (local_player.player_id == current_roller_id)
        roller = next((j for j in joueurs if j.player_id == current_roller_id), local_player)
        roller_name = roller.nom

        if etat_jeu == "SPECTATOR":
            alive_players = [p for p in remote_players.values() if p.vies > 0]
            if local_player.vies > 0: alive_players.append(local_player)
            if not alive_players:
                etat_jeu = "MORT"

        break_to_main_menu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if client: client.disconnect()
                if server: server.stop()
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE | pygame.SCALED)

            if etat_jeu == "LOBBY":
                action, data = lobby_menu.handle_event(event)
                if action == "SEND_CHAT":
                    if client: client.send({"type": "CHAT", "author": local_player.nom, "message": data})
                    else:
                        chat_messages.append(f"{local_player.nom} : {data}")
                        chat_messages = chat_messages[-15:]
                        lobby_menu.set_chat_messages(chat_messages)
                elif action == "START_GAME":
                    if client: client.send({"type": "START_GAME"})
                    else: demarrer_loading()
                elif action == "CHANGE_CHARACTER":
                    local_player.image_path = demander_personnage(ecran, horloge, LARGEUR, HAUTEUR)
                    local_player.charger_image()
                    if client: client.send({"type": "PLAYER_STATE", "id": local_player.player_id, "image_path": local_player.image_path})

            elif etat_jeu == "MORT" or partie_terminee:
                action = death_screen.handle_input(event, mode_solo=(mode_reseau == "SOLO")) if etat_jeu == "MORT" else end_screen.handle_input(event)
                if action == "REJOUER":
                    joueur_actif.reset()
                    joueur_actif.x, joueur_actif.y = 220, 360
                    map_manager.player_pos = [1, 1]
                    map_manager.generate_new_map()
                    central_room.reset_round()
                    partie_terminee = False
                    etat_jeu = "CENTRAL"
                    if "game" in sons: sons["game"].stop()
                    if "intro" in sons: sons["intro"].play(loops=-1)
                elif action == "SPECTATEUR":
                    etat_jeu = "SPECTATOR"
                    spectator_index = 0
                elif action == "MENU_PRINCIPAL":
                    if client: client.disconnect()
                    if server: server.stop()
                    break_to_main_menu = True

            elif etat_jeu == "ENIGME" and puzzle_actif:
                res_txt = puzzle_actif.handle_event(event, local_player)
                if res_txt == "GAGNE":
                    if "win_salle" in sons: sons["win_salle"].play()
                    if "game" in sons: sons["game"].stop()
                    if "intro" in sons: sons["intro"].play(loops=-1)
                    joueur_actif.gagner_points(100)
                    map_manager.quests_completed += 1
                    map_manager.check_exit_condition()
                    central_room.reset_round()
                    etat_jeu = "CENTRAL"
                    puzzle_actif = None
                    for j in joueurs: j.est_bloque = False
                    
                    if est_host:
                        vivants = [p for p in joueurs if p.vies > 0]
                        if vivants:
                            current_roller_id = random.choice(vivants).player_id
                            if client: client.send({"type": "NEW_ROLLER", "roller_id": current_roller_id})
                            
                elif res_txt == "MAUVAISE_REPONSE":
                    if "lose_salle" in sons: sons["lose_salle"].play()
                    joueur_actif.perdre_points(50)
                    joueur_actif.perdre_vie()
                    if joueur_actif.vies <= 0: 
                        if "game" in sons: sons["game"].stop()
                        if "lose_game" in sons: sons["lose_game"].play()
                        etat_jeu = "MORT"

            elif etat_jeu == "CENTRAL" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: minimap.toggle()
                if event.key == pygame.K_e and not local_player.est_bloque:
                    for j in joueurs_meme_salle:
                        if j != local_player and getattr(j, 'est_bloque', False) and local_player.rect.colliderect(j.rect.inflate(60, 60)):
                            local_player.perdre_vie()
                            j.est_bloque = False 
                            
                            if client: 
                                client.send({"type": "UNLOCK_PLAYER", "id": j.player_id})
                                client.send({"type": "PLAYER_STATE", "id": local_player.player_id, "vies": local_player.vies})
                                
                                if est_host:
                                    new_tgt = [random.randint(0,2), random.randint(0,2)]
                                    while new_tgt == list(map_manager.player_pos):
                                        new_tgt = [random.randint(0,2), random.randint(0,2)]
                                        
                                    client.send({"type": "NEW_DESTINATION", "id": j.player_id, "target": new_tgt})
                            
                            if local_player.vies <= 0:
                                etat_jeu = "MORT"

        if break_to_main_menu: break

        if client:
            for message in client.get_messages():
                msg_type = message.get("type")
                if msg_type == "PLAYER_LIST": remplacer_liste_joueurs(message.get("players", []))
                elif msg_type == "START_GAME":
                    if etat_jeu == "LOBBY": demarrer_loading()
                elif msg_type == "MAP_DATA":
                    data = message["map_data"]
                    map_manager.grid = [row[:] for row in data["grid"]]
                    map_manager.player_pos, map_manager.exit_pos = list(data.get("player_pos", [1,1])), list(data.get("exit_pos", [0,0]))
                    map_manager.quests_completed, map_manager.min_quests_to_exit = data.get("quests_completed", 0), data.get("min_quests_to_exit", 2)
                    map_loaded = True
                    if etat_jeu == "LOADING": initialiser_partie()
                elif msg_type == "PLAYER_STATE": update_remote_player(message)
                elif msg_type == "CHAT":
                    chat_messages.append(f"{message['author']} : {message['message']}")
                    chat_messages = chat_messages[-15:]
                    if etat_jeu == "LOBBY": lobby_menu.set_chat_messages(chat_messages)
                elif msg_type == "NEW_ROLLER":
                    current_roller_id = message["roller_id"]
                elif msg_type == "DOOR_OPENED":
                    central_room.open_door(message["index"])
                elif msg_type == "NEW_DESTINATION":
                    if message["id"] == local_player.player_id:
                        central_room.target_coords = message["target"]
                        if message["target"]:
                            lettre = chr(65 + int(message["target"][0]))
                            chiffre = str(int(message["target"][1]) + 1)
                            central_room.target_name = f"Salle {lettre}{chiffre}"
                elif msg_type == "UNLOCK_PLAYER":
                    if message.get("id") == local_player.player_id: local_player.est_bloque = False
                    elif message.get("id") in remote_players: remote_players[message.get("id")].est_bloque = False
                elif msg_type == "SYNC_ROLL":
                    # Récupération de la cible variée attribuée à notre ID par l'hôte
                    tgt_salle = message.get("destinations", {}).get(local_player.player_id, [1,1])
                    central_room.apply_dice_result({
                        "portes": message["portes"], "salle_cible": tgt_salle, "joueurs_requis": message["req_players"]
                    })
                    selected_ids = message["selected_ids"]
                    selected_objs = [p for p in joueurs if p.player_id in selected_ids]
                    de_jeu.roll(message["final_face"], selected_objs, central_room.target_name)
                    etat_jeu = "ROLL_DICE"

        if etat_jeu == "LOBBY":
            lobby_menu.update() 
            lobby_menu.update_players(joueurs)
            lobby_menu.draw(ecran)

        elif etat_jeu == "LOADING":
            if loading_start_time is None: loading_start_time = pygame.time.get_ticks()
            elapsed = pygame.time.get_ticks() - loading_start_time
            if elapsed >= 1600: initialiser_partie()
            dessiner_loading(ecran, LARGEUR, HAUTEUR, elapsed)

        elif etat_jeu == "ROLL_DICE":
            map_manager.draw(ecran)
            central_room.draw(ecran, is_my_turn, roller_name)
            local_player.draw(ecran, font_joueur, actif=True)
            draw_remote_players_same_room(ecran, font_joueur)
            res = de_jeu.update(len(joueurs))
            de_jeu.draw(ecran)
            
            if res is not None or not de_jeu.rolling:
                if mode_reseau == "SOLO":
                    local_player.est_bloque = False
                    local_player.is_selected = True
                else:
                    if local_player.player_id == current_roller_id:
                        local_player.est_bloque = True
                    for j in joueurs:
                        if j.player_id != current_roller_id and j not in de_jeu.selected_players: 
                            j.est_bloque = True
                        elif j.player_id != current_roller_id:
                            j.is_selected = True
                            j.est_bloque = False
                etat_jeu = "CENTRAL"

        elif etat_jeu == "CENTRAL" and not partie_terminee:
            dx = (touches[pygame.K_d] - touches[pygame.K_q]) * local_player.speed
            dy = (touches[pygame.K_s] - touches[pygame.K_z]) * local_player.speed
            local_player.move(dx, dy, 0, LARGEUR, 0, HAUTEUR)

            result = central_room.update(local_player, len(joueurs_meme_salle), is_my_turn, roller_name, can_roll_dice=True)
            if local_player.vies <= 0: etat_jeu = "MORT"
            elif result == "FIN_DU_JEU": partie_terminee = True
            elif result == "START_ROLL":
                central_room.roll_dice(len(joueurs))
                req_players = central_room.required_players
                final_face = req_players if isinstance(req_players, int) else "+"
                nb_a_sel = len(joueurs) if final_face == "+" else min(int(final_face), len(joueurs))
                selected = random.sample(joueurs, nb_a_sel)
                selected_ids = [p.player_id for p in selected]
                
                # 🎲 REPARTITION DES DESTINATIONS SUR LA MAP PAR L'HOTE
                destinations = {}
                base_target = central_room.target_coords
                for j in joueurs:
                    if j.player_id in selected_ids:
                        destinations[j.player_id] = list(base_target)
                    else:
                        alt_target = [random.randint(0,2), random.randint(0,2)]
                        while alt_target == list(base_target):
                            alt_target = [random.randint(0,2), random.randint(0,2)]
                        destinations[j.player_id] = alt_target
                
                # Assigner notre cible locale d'hôte
                local_tgt = destinations[local_player.player_id]
                central_room.target_coords = local_tgt
                lettre = chr(65 + int(local_tgt[0]))
                chiffre = str(int(local_tgt[1]) + 1)
                central_room.target_name = f"Salle {lettre}{chiffre}"
                
                de_jeu.roll(final_face, selected, central_room.target_name)
                etat_jeu = "ROLL_DICE"
                if client:
                    client.send({
                        "type": "SYNC_ROLL", "final_face": final_face, "selected_ids": selected_ids,
                        "destinations": destinations, "portes": central_room.door_dice_results,
                        "req_players": req_players
                    })
            elif result == "LANCER_ENIGME":
                etat_jeu = "ENIGME"
                type_salle = map_manager.get_current_room_type()
                salle_cible = "SURVIVAL_ACIDE" if type_salle == "A" else ("SURVIVAL_PHYSIQUE" if type_salle == "L" else ("OMBRE" if type_salle == "O" else "TEXT"))
                puzzle_actif = PuzzleRoom(room_type=salle_cible, quests_completed=map_manager.quests_completed)
                if "intro" in sons: sons["intro"].stop()
                if "game" in sons: sons["game"].play(loops=-1)

        if client and etat_jeu in ("LOBBY", "CENTRAL", "ENIGME", "ROLL_DICE"):
            client.send({
                "type": "PLAYER_STATE", "id": local_player.player_id, "nom": local_player.nom,
                "x": local_player.x, "y": local_player.y, "score": local_player.score, "vies": local_player.vies,
                "indices_restants": local_player.indices_restants, "est_bloque": getattr(local_player, "est_bloque", False), 
                "facing_right": getattr(local_player, "facing_right", True), "room_pos": map_manager.player_pos[:], 
                "image_path": getattr(local_player, "image_path", None)
            })

        if etat_jeu in ("CENTRAL", "ENIGME", "MORT") and not partie_terminee:
            map_manager.draw(ecran)
            if etat_jeu != "ENIGME":
                central_room.draw(ecran, is_my_turn, roller_name)
                
                for j in joueurs_meme_salle:
                    if j != local_player and getattr(j, 'est_bloque', False):
                        if local_player.rect.colliderect(j.rect.inflate(60, 60)):
                            txt = font_joueur.render("Appuyez sur E pour libérer", True, (255, 255, 0))
                            ecran.blit(txt, (j.x - 30, j.y - 45))

                if central_room.target_coords is not None and map_manager.player_pos is not None:
                    if list(central_room.target_coords) == list(map_manager.player_pos):
                        sorcier.draw(ecran, local_player.rect)
                
                local_player.draw(ecran, font_joueur, actif=True)
                if local_player.est_bloque:
                    pygame.draw.rect(ecran, (255, 0, 0), (local_player.x + local_player.size//2 - 10, local_player.y - 20, 20, 15), border_radius=4)
                    pygame.draw.circle(ecran, (255, 0, 0), (local_player.x + local_player.size//2, local_player.y - 20), 8, 3)
                
                draw_remote_players_same_room(ecran, font_joueur)
                if central_room.dice_rolled: de_jeu.draw_selection_ui(ecran, LARGEUR)
                if etat_jeu == "MORT": death_screen.draw(ecran, mode_solo=(mode_reseau == "SOLO"))
                
            elif etat_jeu == "ENIGME" and puzzle_actif:
                # 🔓 FIX DU BLOCAGE DES JOUEURS : Les mouvements clavier sont réactivés pour tous !
                dx = (touches[pygame.K_d] - touches[pygame.K_q]) * local_player.speed
                dy = (touches[pygame.K_s] - touches[pygame.K_z]) * local_player.speed
                local_player.move(dx, dy, 0, LARGEUR, 0, HAUTEUR)

                if local_player.is_selected:
                    if puzzle_actif.room_type != "TEXT":
                        res_survie = puzzle_actif.update_survival(local_player)
                        if res_survie is True:
                            if "win_salle" in sons: sons["win_salle"].play()
                            if "game" in sons: sons["game"].stop()
                            if "intro" in sons: sons["intro"].play(loops=-1)
                            local_player.gagner_points(100)
                            map_manager.quests_completed += 1
                            map_manager.check_exit_condition()
                            central_room.reset_round()
                            etat_jeu = "CENTRAL"
                            puzzle_actif = None
                            for j in joueurs: j.est_bloque = False
                            
                            if est_host:
                                vivants = [p for p in joueurs if p.vies > 0]
                                if vivants:
                                    current_roller_id = random.choice(vivants).player_id
                                    if client: client.send({"type": "NEW_ROLLER", "roller_id": current_roller_id})
                        elif res_survie is False:
                            if "lose_salle" in sons: sons["lose_salle"].play()
                            if "game" in sons: sons["game"].stop()
                            if "lose_game" in sons: sons["lose_game"].play()
                            etat_jeu = "MORT"
                    if puzzle_actif: puzzle_actif.draw(ecran, local_player, sorcier)
                else:
                    central_room.draw(ecran, is_my_turn, roller_name)
                    local_player.draw(ecran, font_joueur, actif=True)
                    de_jeu.draw_selection_ui(ecran, LARGEUR)

            if etat_jeu != "MORT":
                scoring_system.afficher_hud_score(ecran, joueurs, 0, map_manager)
                lives_manager.afficher_vies(ecran, local_player)
                minimap.draw(ecran)
                # Dessin du bouton Indice en bas à droite
                hud.draw_btn_indice(ecran, local_player.indices_restants)

        elif etat_jeu == "SPECTATOR":
            map_manager.draw(ecran)
            distants = list(remote_players.values())
            if distants:
                if touches[pygame.K_RIGHT]: spectator_index = (spectator_index + 1) % len(distants)
                if touches[pygame.K_LEFT]: spectator_index = (spectator_index - 1) % len(distants)
                cible = distants[spectator_index]
                cible.draw(ecran, font_joueur, actif=True)
                txt_spec = font_titre.render(f"SPECTATEUR : {cible.nom}", True, (255, 255, 0))
                ecran.blit(txt_spec, (LARGEUR//2 - txt_spec.get_width()//2, 20))
            else:
                txt_spec = font_titre.render("AUCUN JOUEUR EN VIE", True, (255, 0, 0))
                ecran.blit(txt_spec, (LARGEUR//2 - txt_spec.get_width()//2, 20))

        elif partie_terminee:
            end_screen.afficher(ecran, joueurs, mode_solo=(mode_reseau == "SOLO"))

        pygame.display.flip()
        horloge.tick(60)