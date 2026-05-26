import pygame
import random
import unicodedata
import math

class PuzzleRoom:
    def __init__(self, room_type="TEXT", largeur=1000, hauteur=700, quests_completed=0):
        self.room_type = room_type
        self.largeur = largeur
        self.hauteur = hauteur
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 28)

        self.etat = "WAITING" 
        self.dialogue = ""
        self.indice_demande = False
        self.indice_texte = ""
        self.erreurs = 0
        self.input_text = ""
        self.creation_time = 0
        self.code_visible_duration_ms = 2500

        if self.room_type == "TEXT":
            self.dialogue = "Le défi mental t'attend. Utilise ton esprit." 
            self.generer_enigme(quests_completed)
            
        elif self.room_type == "SURVIVAL_ACIDE":
            self.dialogue = "Respire un bon coup. Des nuages toxiques arrivent."
            self.start_time = 0
            self.survival_duration, self.countdown_duration = 30000, 3000
            self.projectiles, self.last_spawn_time = [], 0
            self.spawn_rate, self.gas_speed = 750, 4.5 
            self.invincible_until = 0
            self.gas_colors = [(10, 180, 50, 160), (50, 220, 80, 120), (0, 130, 30, 200)]
            
        elif self.room_type == "SURVIVAL_PHYSIQUE":
            self.dialogue = "Le laboratoire est instable. Esquive les lasers."
            self.start_time = 0
            self.survival_duration, self.countdown_duration = 40000, 3000
            self.projectiles, self.last_spawn_time = [], 0
            self.spawn_rate = 1000
            self.invincible_until, self.phase_2_active = 0, False

        elif self.room_type == "OMBRE":
            self.dialogue = "Les ténèbres te consumeront. Reste dans la lumière."
            self.start_time = 0
            self.survival_duration, self.countdown_duration = 20000, 3000
            self.lumiere_x, self.lumiere_y = largeur//2, hauteur//2
            self.lumiere_radius = 180
            self.vx, self.vy = random.choice([-3, 3]), random.choice([-3, 3])
            self.invincible_until = 0
            
        elif self.room_type == "METEORE":
            self.dialogue = "Le sol tremble. Fuis les zones rouges avant l'impact !"
            self.start_time = 0
            self.survival_duration, self.countdown_duration = 25000, 3000
            self.meteores, self.invincible_until = [], 0
            
        try:
            self.chrono_img = pygame.transform.scale(pygame.image.load("assets/chrono.png").convert_alpha(), (200, 100))
        except:
            self.chrono_img = pygame.Surface((200, 100))
            self.chrono_img.fill((50, 0, 0))

    def generer_enigme(self, quests_completed):
        if quests_completed < 3: diff = "facile"
        elif quests_completed < 6: diff = "moyen"
        else: diff = "difficile"

        banque = {
            "facile": [
                {"q": "Je suis grand quand je suis jeune, petit quand je suis vieux.", "r": "bougie", "ind": "On m'allume avec du feu.", "max": 15},
                {"q": "Qu'est-ce qui a des dents mais ne mord pas ?", "r": "peigne", "ind": "On l'utilise pour les cheveux.", "max": 15},
                {"q": "Capitale de l'Espagne ?", "r": "madrid", "ind": "Au centre de la péninsule.", "max": 15},
                {"q": "Calcule : 15 + 27 =", "r": "42", "ind": "La réponse à l'univers.", "max": 5},
                {"q": "Calcule : 50 - 15 =", "r": "35", "ind": "Soustraction simple.", "max": 5},
                {"q": "Je suis plein de trous mais je retiens l'eau.", "r": "eponge", "ind": "Utile sous l'évier.", "max": 15},
                {"q": "Qu'est-ce qui a un cou mais pas de tête ?", "r": "bouteille", "ind": "Contient un liquidessssssss.", "max": 15},
                {"q": "Plus je sèche, plus je suis mouillée. Qui suis-je ?", "r": "serviette", "ind": "Après le bain.", "max": 15},
                {"q": "Capitale de l'Italie ?", "r": "rome", "ind": "Proche du Colisée.", "max": 15},
                {"q": "Calcule : 9 * 4 =", "r": "36", "ind": "Table de multiplication.", "max": 5}
            ],
            "moyen": [
                {"q": "Je parle sans bouche et j'entends sans oreilles.", "r": "echo", "ind": "Je répète dans les montagnes.", "max": 15},
                {"q": "Je tombe sans me faire mal, je coule sans me noyer.", "r": "pluie", "ind": "Elle vient du ciel.", "max": 15},
                {"q": "Combien de mois dans l'année ont 28 jours ?", "r": "12", "ind": "Tous les mois !", "max": 5},
                {"q": "Calcule : 8 * 7 - 6 =", "r": "50", "ind": "Nombre rond.", "max": 5},
                {"q": "Qu'est-ce qui est à toi mais que les autres utilisent plus ?", "r": "nom", "ind": "Ton identité.", "max": 15},
                {"q": "On la tourne pour avancer, mais ce n'est pas une roue.", "r": "page", "ind": "Dans les bouquins.", "max": 15},
                {"q": "Qu'est ce qui disparaît dès qu'on prononce son nom ?", "r": "silence", "ind": "Chut...", "max": 15},
                {"q": "Je ne respire jamais, mais j'ai beaucoup de souffle.", "r": "vent", "ind": "Agite les arbres.", "max": 15},
                {"q": "Calcule : (15 * 2) + 14 =", "r": "44", "ind": "Priorité aux parenthèses.", "max": 5},
                {"q": "Sans moi, Paris serait pris.", "r": "a", "ind": "C'est une voyelle.", "max": 5}
            ],
            "difficile": [
                {"q": "Toujours devant toi, mais tu ne peux jamais me voir.", "r": "avenir", "ind": "Le futur.", "max": 15},
                {"q": "Si tu me nourris je vis, si tu me donnes à boire je meurs.", "r": "feu", "ind": "Éléments destructeur et chaud.", "max": 15},
                {"q": "Je peux remplir une pièce sans prendre de place.", "r": "lumiere", "ind": "Chasse l'obscurité.", "max": 15},
                {"q": "Plus on en retire, plus je grandis.", "r": "trou", "ind": "Creusé au sol.", "max": 15},
                {"q": "Je commence la nuit et je finis le matin.", "r": "n", "ind": "Observe bien la première lettre.", "max": 5},
                {"q": "Calcule : 144 / 12 =", "r": "12", "ind": "Division parfaite.", "max": 5},
                {"q": "On me donne, on me prend, mais on ne me garde jamais.", "r": "parole", "ind": "Tenir sa promesse.", "max": 15},
                {"q": "Retiens puis tape ce code : " + str(random.randint(10000, 99999)), "r": "MEMOIRE", "ind": "Observe le code au début.", "max": 10},
                {"q": "Retiens puis tape ce code : " + str(random.randint(10000, 99999)), "r": "MEMOIRE", "ind": "Pas d'erreur possible.", "max": 10},
                {"q": "Retiens puis tape ce code : " + str(random.randint(10000, 99999)), "r": "MEMOIRE", "ind": "Dernière ligne droite.", "max": 10}
            ]
        }

        enigme = random.choice(banque[diff])
        if enigme["r"] == "MEMOIRE":
            code = enigme["q"].split(" : ")[1]
            self.question = "Retiens ce code puis retape-le !"
            self.reponse = code
            self.instruction = "Le code disparaît rapidement."
            self.type = 2 
        else:
            self.question = enigme["q"]
            self.reponse = enigme["r"]
            self.instruction = "Écris la réponse puis appuie sur ENTRÉE"
            self.type = 0 
            
        self.indice_texte = enigme["ind"]
        self.max_input_len = enigme["max"]

    def declencher_aide_urgence(self):
        secours = [
            {"q": "AIDE D'URGENCE : 2 + 2 =", "r": "4", "ind": "Addition simple.", "max": 5},
            {"q": "AIDE D'URGENCE : 10 - 3 =", "r": "7", "ind": "Soustraction.", "max": 5},
            {"q": "AIDE D'URGENCE : 5 * 2 =", "r": "10", "ind": "La moitié de vingt.", "max": 5}
        ]
        enigme = random.choice(secours)
        self.question = enigme["q"]
        self.reponse = enigme["r"]
        self.indice_texte = enigme["ind"]
        self.max_input_len = enigme["max"]
        self.type = 0
        self.input_text = ""
        self.indice_demande = False

    def _normalize_text(self, text):
        text = text.strip().lower()
        text = unicodedata.normalize("NFD", text)
        return "".join(char for char in text if unicodedata.category(char) != "Mn")

    def _is_correct_answer(self):
        return self._normalize_text(self.input_text) == self._normalize_text(self.reponse)

    def _creer_nuage(self, x, y):
        radius = 45 
        particles = []
        for _ in range(12):
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(0, radius * 0.7)
            px = math.cos(angle) * dist
            py = math.sin(angle) * dist
            p_radius = random.uniform(15, 25)
            color = random.choice(self.gas_colors)
            speed_rot = random.uniform(-0.05, 0.05) 
            particles.append({"rel_x": px, "rel_y": py, "radius": p_radius, "base_radius": p_radius, "color": color, "angle": angle, "dist": dist, "speed_rot": speed_rot})
        return {"x": x, "y": y, "radius": radius, "particles": particles, "rect": pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)}

    def _creer_laser(self):
        horizontal = random.choice([True, False])
        couleur = (255, 50, 50) if not self.phase_2_active else (50, 200, 255)
        vitesse = random.uniform(7, 10) if not self.phase_2_active else random.uniform(11, 16)
        if horizontal:
            y = random.randint(150, 650)
            sens = random.choice([1, -1])
            x = -200 if sens == 1 else 1100
            return {"rect": pygame.Rect(x, y, 300, 20), "dx": vitesse * sens, "dy": 0, "color": couleur}
        else:
            x = random.randint(50, 950)
            sens = random.choice([1, -1])
            y = -200 if sens == 1 else 800
            return {"rect": pygame.Rect(x, y, 20, 300), "dx": 0, "dy": vitesse * sens, "color": couleur}

    def handle_event(self, event, player=None):
        if self.etat == "WAITING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.etat = "DIALOGUE"
                if player:
                    player.x = self.largeur//2 - player.size//2
                    player.y = self.hauteur//2 + 50
                    player.rect.topleft = (player.x, player.y)
            return None

        if self.etat == "DIALOGUE":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.room_type == "TEXT":
                    self.etat = "PLAYING"
                    self.creation_time = pygame.time.get_ticks()
                else:
                    self.etat = "COUNTDOWN"
                    self.start_time = pygame.time.get_ticks()
            return None

        if self.room_type == "TEXT" and self.etat == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_rect = pygame.Rect(self.largeur - 150, 20, 130, 40)
                if btn_rect.collidepoint(event.pos):
                    if player and getattr(player, 'indices_restants', 0) > 0 and not self.indice_demande:
                        self.indice_demande = True
                        player.indices_restants -= 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: 
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self._is_correct_answer(): 
                        return "GAGNE"
                    else: 
                        self.erreurs += 1
                        self.input_text = ""
                        if self.erreurs >= 3: 
                            self.declencher_aide_urgence()
                        return "MAUVAISE_REPONSE"
                else:
                    if event.unicode.isprintable() and len(self.input_text) < self.max_input_len:
                        self.input_text += event.unicode
        return None

    def update_survival(self, player):
        if self.etat in ("WAITING", "DIALOGUE"): return None
        
        now = pygame.time.get_ticks()
        elapsed_total = now - self.start_time
        keys = pygame.key.get_pressed()
        
        if self.etat == "COUNTDOWN":
            if elapsed_total > self.countdown_duration:
                self.etat = "PLAYING"
                self.start_time = now
            return None
            
        elif self.etat == "PLAYING":
            elapsed_playing = now - self.start_time
            time_left_ms = max(0, self.survival_duration - elapsed_playing)
            
            if time_left_ms == 0: return True
                
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_q]: dx -= player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += player.speed
            if keys[pygame.K_UP] or keys[pygame.K_z]: dy -= player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += player.speed
            player.move(dx, dy, 0, self.largeur, 0, self.hauteur)

            if self.room_type == "SURVIVAL_ACIDE":
                if now - self.last_spawn_time > self.spawn_rate:
                    self.last_spawn_time = now
                    self.projectiles.append(self._creer_nuage(random.randint(50, self.largeur-50), -60))
                t = now / 1000.0
                for cloud in self.projectiles[:]:
                    cloud["y"] += self.gas_speed
                    cloud["rect"].y = int(cloud["y"] - cloud["radius"])
                    for p in cloud["particles"]:
                        p["angle"] += p["speed_rot"]
                        p["rel_x"] = math.cos(p["angle"]) * p["dist"]
                        p["rel_y"] = math.sin(p["angle"]) * p["dist"]
                        p["radius"] = p["base_radius"] + math.sin(t * 5 + p["dist"]) * 2

                    if cloud["y"] > self.hauteur + 100: 
                        self.projectiles.remove(cloud)
                    elif cloud["rect"].colliderect(player.rect):
                        if now > self.invincible_until:
                            player.perdre_vie()
                            self.invincible_until = now + 3000
                            if player.vies <= 0: return False

            elif self.room_type == "SURVIVAL_PHYSIQUE":
                if elapsed_playing > 12000 and not self.phase_2_active:
                    self.phase_2_active = True
                    self.spawn_rate = 500 
                if now - self.last_spawn_time > self.spawn_rate:
                    self.last_spawn_time = now
                    self.projectiles.append(self._creer_laser())
                for laser in self.projectiles[:]:
                    laser["rect"].x += laser["dx"]
                    laser["rect"].y += laser["dy"]
                    if laser["rect"].x > self.largeur + 200 or laser["rect"].x < -300 or laser["rect"].y > self.hauteur + 200 or laser["rect"].y < -300:
                        self.projectiles.remove(laser)
                    elif laser["rect"].colliderect(player.rect):
                        if now > self.invincible_until:
                            player.perdre_vie()
                            self.invincible_until = now + 3000
                            if player.vies <= 0: return False

            elif self.room_type == "OMBRE":
                self.lumiere_x += self.vx
                self.lumiere_y += self.vy
                if self.lumiere_x < 0 or self.lumiere_x > self.largeur: self.vx *= -1
                if self.lumiere_y < 0 or self.lumiere_y > self.hauteur: self.vy *= -1
                dist = math.hypot((player.x + player.size//2) - self.lumiere_x, (player.y + player.size//2) - self.lumiere_y)
                if dist > self.lumiere_radius:
                    if now > getattr(self, "invincible_until", 0):
                        player.perdre_vie()
                        self.invincible_until = now + 1000 
                        if player.vies <= 0: return False

            elif self.room_type == "METEORE":
                if random.randint(1, 20) == 1:
                    self.meteores.append({"x": random.randint(100, self.largeur-100), "y": random.randint(100, self.hauteur-100), "radius": 100, "timer": 60})
                for m in self.meteores[:]:
                    m["timer"] -= 1
                    if m["timer"] <= 0:
                        dist = math.hypot((player.x + player.size//2) - m["x"], (player.y + player.size//2) - m["y"])
                        if dist < m["radius"]:
                            player.perdre_vie()
                            if player.vies <= 0: return False
                        self.meteores.remove(m)
        return None

    def draw(self, screen, player=None, sorcier=None):
        now = pygame.time.get_ticks()

        if self.etat == "WAITING":
            overlay = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
            overlay.fill((10, 10, 20, 150)) 
            screen.blit(overlay, (0, 0))
            txt = self.font.render("Le Maître vous attend au centre...", True, (255, 255, 255))
            screen.blit(txt, (self.largeur//2 - txt.get_width()//2, 80))
            txt2 = self.font_small.render("Approchez et appuyez sur 'E'", True, (200, 200, 200))
            screen.blit(txt2, (self.largeur//2 - txt2.get_width()//2, 120))
            if sorcier: sorcier.draw(screen, player.rect if player else None)
            if player: player.draw(screen, self.font_small, actif=True)
            return

        if self.etat == "DIALOGUE":
            screen.fill((15, 15, 20))
            txt_pret = self.font_big.render("Le Maître : Es-tu prêt ?", True, (0, 255, 255))
            screen.blit(txt_pret, (self.largeur//2 - txt_pret.get_width()//2, self.hauteur//2 - 80))
            txt_diag = self.font.render(self.dialogue, True, (200, 255, 255))
            screen.blit(txt_diag, (self.largeur//2 - txt_diag.get_width()//2, self.hauteur//2))
            txt2 = self.font.render("-> Appuie sur ESPACE pour commencer <-", True, (200, 200, 200))
            screen.blit(txt2, (self.largeur//2 - txt2.get_width()//2, self.hauteur//2 + 80))
            return

        overlay = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 230)) 
        screen.blit(overlay, (0, 0))

        txt_info = self.font_small.render("Seule la réponse te libérera", True, (150, 50, 50))
        screen.blit(txt_info, (20, 20))

        if self.room_type == "TEXT":
            titre = self.font_big.render("DÉFI MENTAL", True, (255, 215, 0))
            screen.blit(titre, (self.largeur // 2 - titre.get_width() // 2, 80))
            
            indices = getattr(player, 'indices_restants', 0) if player else 0
            btn_rect = pygame.Rect(self.largeur - 150, 20, 130, 40)
            mx, my = pygame.mouse.get_pos()
            hover = btn_rect.collidepoint(mx, my)
            btn_color = (200, 200, 50) if hover and indices > 0 else ((100, 100, 50) if indices == 0 else (150, 150, 0))
            pygame.draw.rect(screen, btn_color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=8)
            txt_btn = self.font_small.render(f"? Indice ({indices})", True, (0, 0, 0))
            screen.blit(txt_btn, (btn_rect.centerx - txt_btn.get_width()//2, btn_rect.centery - txt_btn.get_height()//2))
            
            if self.indice_demande:
                txt_i = self.font_small.render(f"INDICE : {self.indice_texte}", True, (0, 255, 255))
                screen.blit(txt_i, (self.largeur // 2 - txt_i.get_width() // 2, 160))
                
            lbl_q = self.font.render(self.question, True, (255, 255, 255))
            screen.blit(lbl_q, (self.largeur // 2 - lbl_q.get_width() // 2, 220))
            
            if hasattr(self, 'type') and self.type == 2:
                elapsed = pygame.time.get_ticks() - self.creation_time
                indice = self.font.render(f"CODE : {self.reponse}" if elapsed <= self.code_visible_duration_ms else "CODE MASQUÉ", True, (255, 255, 255) if elapsed <= self.code_visible_duration_ms else (120, 120, 120))
                screen.blit(indice, (self.largeur // 2 - indice.get_width() // 2, 280))
                
            input_box = pygame.Rect(self.largeur // 2 - 160, 380, 320, 55)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            txt_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(txt_surface, (input_box.x + 12, input_box.y + 10))
            
            if hasattr(self, 'instruction'):
                info = self.font_small.render(self.instruction, True, (170, 170, 170))
                screen.blit(info, (self.largeur // 2 - info.get_width() // 2, 455))
        else:
            if self.room_type == "SURVIVAL_ACIDE":
                for cloud in self.projectiles:
                    surf_size = int(cloud["radius"] * 2 + 30)
                    cloud_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
                    center_s = surf_size // 2
                    for p in cloud["particles"]:
                        px, py = int(center_s + p["rel_x"]), int(center_s + p["rel_y"])
                        pygame.draw.circle(cloud_surf, p["color"], (px, py), int(p["radius"]))
                    screen.blit(cloud_surf, (int(cloud["x"] - center_s), int(cloud["y"] - center_s)))
                    
            elif self.room_type == "SURVIVAL_PHYSIQUE":
                for laser in self.projectiles:
                    pygame.draw.rect(screen, laser["color"], laser["rect"], border_radius=10)
                    halo_rect = laser["rect"].inflate(10, 10)
                    halo_surf = pygame.Surface((halo_rect.width, halo_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(halo_surf, (laser["color"][0], laser["color"][1], laser["color"][2], 100), halo_surf.get_rect(), border_radius=15)
                    screen.blit(halo_surf, halo_rect)
                    
            elif self.room_type == "OMBRE":
                surf = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
                surf.fill((0, 0, 0, 240)) 
                pygame.draw.circle(surf, (0, 0, 0, 0), (int(self.lumiere_x), int(self.lumiere_y)), self.lumiere_radius)
                screen.blit(surf, (0, 0))
                pygame.draw.circle(screen, (255, 255, 200), (int(self.lumiere_x), int(self.lumiere_y)), self.lumiere_radius, 2)
                
            elif self.room_type == "METEORE":
                for m in self.meteores:
                    color = (255, 0, 0) if m["timer"] < 15 else (150, 50, 50)
                    pygame.draw.circle(screen, color, (m["x"], m["y"]), m["radius"])

            if player:
                if now < getattr(self, "invincible_until", 0):
                    if (now // 200) % 2 == 0: player.draw(screen, self.font_small, actif=True)
                else: player.draw(screen, self.font_small, actif=True)

            screen.blit(self.chrono_img, (self.largeur // 2 - 100, 10))
            if self.etat == "COUNTDOWN":
                time_left = max(0, self.countdown_duration - (now - self.start_time))
                seconds = int((time_left / 1000) + 1)
                txt = "GO!" if time_left == 0 else str(min(seconds, 3))
                lbl = self.font_big.render(txt, True, (255, 50, 50) if seconds == 1 else (255, 255, 255))
                screen.blit(lbl, (self.largeur // 2 - lbl.get_width() // 2, 130))
            elif self.etat == "PLAYING":
                time_left = max(0, self.survival_duration - (now - self.start_time))
                chrono_txt = self.font_big.render(f"00:{int(time_left / 1000):02d}", True, (255, 0, 0))
                screen.blit(chrono_txt, (self.largeur // 2 - chrono_txt.get_width() // 2, 40))