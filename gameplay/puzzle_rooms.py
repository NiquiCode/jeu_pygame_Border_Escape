import pygame
import random
import unicodedata
import math

class PuzzleRoom:
    def __init__(self, room_type="TEXT", largeur=1000, hauteur=700):
        self.room_type = room_type
        self.largeur = largeur
        self.hauteur = hauteur
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 28)

        self.etat = "DIALOGUE" if room_type != "TEXT" else "PLAYING"
        self.dialogue = ""

        self.indice_demande = False
        self.indice_texte = ""

        if self.room_type == "TEXT":
            self.type = random.randint(0, 2)
            self.question = ""
            self.reponse = ""
            self.instruction = ""
            self.max_input_len = 12
            self.generer_enigme()
            self.input_text = ""
            self.creation_time = pygame.time.get_ticks()
            self.code_visible_duration_ms = 2500
            
        elif self.room_type == "SURVIVAL_ACIDE":
            self.dialogue = "Le Maître : Respire un bon coup. Des nuages toxiques arrivent."
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 30000 
            self.countdown_duration = 3000  
            self.projectiles = []
            self.last_spawn_time = 0
            self.spawn_rate = 750  
            self.gas_speed = 4.5    
            self.invincible_until = 0
            self.gas_colors = [(10, 180, 50, 160), (50, 220, 80, 120), (0, 130, 30, 200)]
            
        elif self.room_type == "SURVIVAL_PHYSIQUE":
            self.dialogue = "Le Maître : Le laboratoire est instable. Esquive les lasers."
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 40000 
            self.countdown_duration = 3000  
            self.projectiles = []
            self.last_spawn_time = 0
            self.spawn_rate = 1000
            self.invincible_until = 0
            self.phase_2_active = False

        elif self.room_type == "OMBRE":
            self.dialogue = "Le Maître : Les ténèbres te consumeront. Reste dans la lumière."
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 20000
            self.countdown_duration = 3000
            self.lumiere_x, self.lumiere_y = largeur//2, hauteur//2
            self.lumiere_radius = 180
            self.vx, self.vy = random.choice([-6, 6]), random.choice([-6, 6])
            self.invincible_until = 0
            
        elif self.room_type == "METEORE":
            self.dialogue = "Le Maître : Le sol tremble. Fuis les zones rouges avant l'impact !"
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 25000
            self.countdown_duration = 3000
            self.meteores = []
            self.invincible_until = 0
            
        try:
            self.chrono_img = pygame.image.load("assets/chrono.png").convert_alpha()
            self.chrono_img = pygame.transform.scale(self.chrono_img, (200, 100))
        except FileNotFoundError:
            self.chrono_img = pygame.Surface((200, 100))
            self.chrono_img.fill((50, 0, 0))

    def generer_enigme(self):
        if self.type == 0:
            data = {
                "France": ("Paris", "C'est la ville de l'amour."),
                "Italie": ("Rome", "On y trouve le Colisée."),
                "Espagne": ("Madrid", "Au centre de la péninsule ibérique."),
                "Angleterre": ("Londres", "Big Ben y sonne."),
                "Allemagne": ("Berlin", "Autrefois coupée par un mur.")
            }
            pays = random.choice(list(data.keys()))
            self.question = f"Capitale de : {pays} ?"
            self.reponse, self.indice_texte = data[pays]
            self.instruction = "Écris la capitale puis appuie sur ENTRÉE"
            self.max_input_len = 20

        elif self.type == 1:
            a, b = random.randint(2, 12), random.randint(2, 12)
            op = random.choice(["+", "-", "*"])
            if op == "+": res = a + b
            elif op == "-": res = a - b
            else: res = a * b
            self.question = f"Calcule : {a} {op} {b} ="
            self.reponse = str(res)
            self.indice_texte = f"Le résultat est proche de {res + random.choice([-2, 2])}."
            self.instruction = "Écris le résultat puis appuie sur ENTRÉE"
            self.max_input_len = 10

        else:
            code = str(random.randint(1000, 9999))
            self.question = "Retiens ce code puis retape-le"
            self.reponse = code
            self.indice_texte = f"Le code commence par {code[0]}."
            self.instruction = "Le code disparaît rapidement. Retape-le puis ENTRÉE"
            self.max_input_len = 10

    def _normalize_text(self, text):
        text = text.strip().lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        return text

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
        if self.etat == "DIALOGUE":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player:
                self.etat = "COUNTDOWN"
                self.start_time = pygame.time.get_ticks()
                player.x, player.y = self.largeur//2 - player.size//2, self.hauteur//2 - player.size//2
                player.rect.topleft = (player.x, player.y)
            return None

        if self.room_type == "TEXT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "QUITTER"
                elif event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self._is_correct_answer(): return "GAGNE"
                    else: self.input_text = ""; return "PERDU"
                else:
                    if event.unicode.isprintable() and len(self.input_text) < self.max_input_len:
                        self.input_text += event.unicode
        return None

    def update_survival(self, player):
        if self.etat == "DIALOGUE": return None
        
        now = pygame.time.get_ticks()
        elapsed_total = now - self.start_time
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]: return "QUITTER"

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

                    if cloud["y"] > self.hauteur + 100: self.projectiles.remove(cloud)
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
                    if now > self.invincible_until:
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

    def draw(self, screen, player=None):
        now = pygame.time.get_ticks()

        if self.etat == "DIALOGUE":
            screen.fill((15, 15, 20))
            txt = self.font.render(self.dialogue, True, (0, 255, 255))
            screen.blit(txt, (self.largeur//2 - txt.get_width()//2, self.hauteur//2 - 40))
            txt2 = self.font.render("-> Appuie sur ESPACE pour commencer l'épreuve <-", True, (200, 200, 200))
            screen.blit(txt2, (self.largeur//2 - txt2.get_width()//2, self.hauteur//2 + 40))
            return

        overlay = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 230)) 
        screen.blit(overlay, (0, 0))

        txt_quit = self.font_small.render("[ESC] QUITTER", True, (150, 150, 150))
        screen.blit(txt_quit, (20, 20))

        if self.room_type == "TEXT":
            titre = self.font_big.render("L'ÉPREUVE DU SORCIER", True, (255, 215, 0))
            screen.blit(titre, (self.largeur // 2 - titre.get_width() // 2, 80))
            if self.indice_demande:
                txt_i = self.font_small.render(f"CONSEIL : {self.indice_texte}", True, (0, 255, 150))
                screen.blit(txt_i, (self.largeur // 2 - txt_i.get_width() // 2, 150))
            lbl_q = self.font.render(self.question, True, (255, 255, 255))
            screen.blit(lbl_q, (self.largeur // 2 - lbl_q.get_width() // 2, 220))
            if self.type == 2:
                elapsed = pygame.time.get_ticks() - self.creation_time
                indice = self.font.render(f"CODE : {self.reponse}" if elapsed <= self.code_visible_duration_ms else "CODE MASQUÉ", True, (255, 255, 255) if elapsed <= self.code_visible_duration_ms else (120, 120, 120))
                screen.blit(indice, (self.largeur // 2 - indice.get_width() // 2, 280))
            input_box = pygame.Rect(self.largeur // 2 - 160, 380, 320, 55)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            txt_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(txt_surface, (input_box.x + 12, input_box.y + 10))
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
                if now < self.invincible_until:
                    if (now // 200) % 2 == 0: player.draw(screen, self.font_small, actif=True)
                else:
                    player.draw(screen, self.font_small, actif=True)

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