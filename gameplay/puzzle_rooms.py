import pygame
import random
import unicodedata
import math

class PuzzleRoom:
    def __init__(self, room_type="TEXT"):
        self.room_type = room_type
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 28)

        # Variables pour les indices de l'IA
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
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 30000 
            self.countdown_duration = 3000  
            self.state = "COUNTDOWN"  
            self.projectiles = []
            self.last_spawn_time = 0
            self.spawn_rate = 750  
            self.gas_speed = 4.5    
            self.invincible_until = 0
            self.gas_colors = [
                (10, 180, 50, 160), (50, 220, 80, 120), (0, 130, 30, 200)
            ]
            
        elif self.room_type == "SURVIVAL_PHYSIQUE":
            # --- MODIFICATION : Plus intense ! ---
            self.start_time = pygame.time.get_ticks()
            self.survival_duration = 40000 
            self.countdown_duration = 3000  
            self.state = "COUNTDOWN"  
            self.projectiles = []
            self.last_spawn_time = 0
            self.spawn_rate = 1000 # Spawn légèrement plus rapide (1.2s -> 1s)
            self.invincible_until = 0
            self.phase_2_active = False
            
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
            a = random.randint(2, 12)
            b = random.randint(2, 12)
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
            particles.append({
                "rel_x": px, "rel_y": py, "radius": p_radius, "base_radius": p_radius, 
                "color": color, "angle": angle, "dist": dist, "speed_rot": speed_rot
            })
        return {"x": x, "y": y, "radius": radius, "particles": particles, "rect": pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)}

    def _creer_laser(self):
        horizontal = random.choice([True, False])
        couleur = (255, 50, 50) if not self.phase_2_active else (50, 200, 255)
        
        # --- MODIFICATION : Vitesse DOUBLÉE ! ---
        # Phase 1: 7-10 pixels/frame (Rapide)
        # Phase 2: 11-16 pixels/frame (Extrêmement rapide)
        vitesse = random.uniform(7, 10) if not self.phase_2_active else random.uniform(11, 16)
        
        if horizontal:
            y = random.randint(150, 650)
            sens = random.choice([1, -1])
            x = -200 if sens == 1 else 1100
            rect = pygame.Rect(x, y, 300, 20)
            return {"rect": rect, "dx": vitesse * sens, "dy": 0, "color": couleur}
        else:
            x = random.randint(50, 950)
            sens = random.choice([1, -1])
            y = -200 if sens == 1 else 800
            rect = pygame.Rect(x, y, 20, 300)
            return {"rect": rect, "dx": 0, "dy": vitesse * sens, "color": couleur}

    def handle_event(self, event, player=None):
        if self.room_type == "TEXT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUITTER"
                elif event.key == pygame.K_BACKSPACE: 
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self._is_correct_answer(): return "GAGNE"
                    else:
                        self.input_text = ""
                        return "PERDU"
                else:
                    if event.unicode.isprintable() and len(self.input_text) < self.max_input_len:
                        self.input_text += event.unicode
        return None

    def update_survival(self, player):
        now = pygame.time.get_ticks()
        elapsed_total = now - self.start_time
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return "QUITTER"

        if self.state == "COUNTDOWN":
            if elapsed_total > self.countdown_duration:
                self.state = "PLAYING"
                self.start_time = now
            return None
            
        elif self.state == "PLAYING":
            elapsed_playing = now - self.start_time
            time_left_ms = max(0, self.survival_duration - elapsed_playing)
            
            if time_left_ms == 0:
                self.state = "FINISHED"
                return True
                
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_q]: dx -= player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += player.speed
            if keys[pygame.K_UP] or keys[pygame.K_z]: dy -= player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += player.speed
                
            player.move(dx, dy)
            player.update()

            if self.room_type == "SURVIVAL_ACIDE":
                if now - self.last_spawn_time > self.spawn_rate:
                    self.last_spawn_time = now
                    x_pos = random.randint(50, 950)
                    self.projectiles.append(self._creon_nuage(x_pos, -60))
                    
                t = now / 1000.0
                for cloud in self.projectiles[:]:
                    cloud["y"] += self.gas_speed
                    cloud["rect"].y = int(cloud["y"] - cloud["radius"])
                    
                    for p in cloud["particles"]:
                        p["angle"] += p["speed_rot"]
                        p["rel_x"] = math.cos(p["angle"]) * p["dist"]
                        p["rel_y"] = math.sin(p["angle"]) * p["dist"]
                        p["radius"] = p["base_radius"] + math.sin(t * 5 + p["dist"]) * 2

                    if cloud["y"] > 800:
                        self.projectiles.remove(cloud)
                    elif cloud["rect"].colliderect(player.rect):
                        if now > self.invincible_until:
                            player.perdre_vie()
                            self.invincible_until = now + 3000
                            if player.vies <= 0: return False

            elif self.room_type == "SURVIVAL_PHYSIQUE":
                # Vérification de la Phase 2 (rythme accéléré après 12s)
                if elapsed_playing > 12000 and not self.phase_2_active:
                    self.phase_2_active = True
                    # Les lasers spawnent 2x plus vite (500ms) !
                    self.spawn_rate = 500 
                
                if now - self.last_spawn_time > self.spawn_rate:
                    self.last_spawn_time = now
                    self.projectiles.append(self._creer_laser())
                    
                for laser in self.projectiles[:]:
                    laser["rect"].x += laser["dx"]
                    laser["rect"].y += laser["dy"]
                    
                    if laser["rect"].x > 1200 or laser["rect"].x < -300 or laser["rect"].y > 900 or laser["rect"].y < -300:
                        self.projectiles.remove(laser)
                    else:
                        if laser["rect"].colliderect(player.rect):
                            if now > self.invincible_until:
                                player.perdre_vie()
                                self.invincible_until = now + 3000
                                if player.vies <= 0: return False
            
        return None

    def draw(self, screen, player=None):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 230)) # Légèrement transparent
        screen.blit(overlay, (0, 0))

        txt_quit = self.font_small.render("[ESC] QUITTER", True, (150, 150, 150))
        screen.blit(txt_quit, (20, 20))

        if self.room_type == "TEXT":
            # --- DESSIN DU SORCIER DANS L'ÉCRAN D'ÉNIGME ---
            sorcier_rect = pygame.Rect(750, 350, 100, 150)
            pygame.draw.rect(screen, (40, 0, 80), sorcier_rect, border_radius=15) # Robe
            
            tête_centre = (sorcier_rect.centerx, sorcier_rect.y + 40)
            pygame.draw.circle(screen, (255, 220, 180), tête_centre, 35) # Tête
            
            # Yeux
            pygame.draw.circle(screen, (0, 0, 0), (tête_centre[0] - 12, tête_centre[1] - 5), 4)
            pygame.draw.circle(screen, (0, 0, 0), (tête_centre[0] + 12, tête_centre[1] - 5), 4)
            
            # --- LA BARBE POINTUE ---
            barbe_coords = [
                (tête_centre[0] - 30, tête_centre[1] + 15), # Haut Gauche
                (tête_centre[0] + 30, tête_centre[1] + 15), # Haut Droite
                (tête_centre[0], tête_centre[1] + 90)     # Pointe
            ]
            pygame.draw.polygon(screen, (240, 240, 240), barbe_coords)
            
            # --- LE BUREAU REMPLI ---
            bureau_rect = pygame.Rect(650, 470, 300, 100)
            pygame.draw.rect(screen, (100, 70, 40), bureau_rect, border_radius=10) # Bois
            
            # Grimoire
            livre_rect = pygame.Rect(670, 450, 60, 40)
            pygame.draw.rect(screen, (150, 50, 50), livre_rect, border_radius=5)
            pygame.draw.rect(screen, (255, 255, 255), livre_rect, 2, border_radius=5)
            
            # Potion
            pos_pot = (800, 455)
            pygame.draw.circle(screen, (50, 255, 100), pos_pot, 20) # Liquide vert
            pygame.draw.rect(screen, (200, 200, 200), (pos_pot[0]-5, pos_pot[1]-35, 10, 15), border_radius=3) # Bouchon

            # Dessin de l'énigme classique
            titre = self.font_big.render("L'ÉPREUVE DU SORCIER", True, (255, 215, 0))
            screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, 80))
            
            if self.indice_demande:
                txt_i = self.font_small.render(f"CONSEIL : {self.indice_texte}", True, (0, 255, 150))
                screen.blit(txt_i, (screen.get_width() // 2 - txt_i.get_width() // 2, 150))

            lbl_q = self.font.render(self.question, True, (255, 255, 255))
            screen.blit(lbl_q, (screen.get_width() // 2 - lbl_q.get_width() // 2, 220))
            
            if self.type == 2:
                elapsed = pygame.time.get_ticks() - self.creation_time
                if elapsed <= self.code_visible_duration_ms:
                    indice = self.font.render(f"CODE : {self.reponse}", True, (255, 255, 255))
                else:
                    indice = self.font.render("CODE MASQUÉ", True, (120, 120, 120))
                screen.blit(indice, (screen.get_width() // 2 - indice.get_width() // 2, 280))
                
            input_box = pygame.Rect(screen.get_width() // 2 - 160, 380, 320, 55)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            txt_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(txt_surface, (input_box.x + 12, input_box.y + 10))
            info = self.font_small.render(self.instruction, True, (170, 170, 170))
            screen.blit(info, (screen.get_width() // 2 - info.get_width() // 2, 455))

        else:
            # Dessin de la survie
            if self.room_type == "SURVIVAL_ACIDE":
                # ... Dessin acide identique ...
                pass
            elif self.room_type == "SURVIVAL_PHYSIQUE":
                for laser in self.projectiles:
                    pygame.draw.rect(screen, laser["color"], laser["rect"], border_radius=10)
                    halo_rect = laser["rect"].inflate(10, 10)
                    halo_color = (laser["color"][0], laser["color"][1], laser["color"][2], 100)
                    halo_surf = pygame.Surface((halo_rect.width, halo_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(halo_surf, halo_color, halo_surf.get_rect(), border_radius=15)
                    screen.blit(halo_surf, halo_rect)

            if player:
                if now < self.invincible_until:
                    if (now // 200) % 2 == 0:
                        player.draw(screen, self.font_small, actif=True)
                else:
                    player.draw(screen, self.font_small, actif=True)

            screen.blit(self.chrono_img, (screen.get_width() // 2 - 100, 10))
            
            # ... Dessin countdown ...