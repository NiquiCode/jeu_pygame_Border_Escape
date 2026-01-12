import pygame
import random

class PuzzleRoom:
    def __init__(self):
        # 0 = Géo, 1 = Math, 2 = Code
        self.type = random.randint(0, 2)
        self.question, self.reponse = self.generer_enigme()
        self.input_text = ""
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        
        self.message_resultat = "" # Pour afficher "Raté" ou "Bravo" brièvement

    def generer_enigme(self):
        if self.type == 0: # Capitales
            data = {"France": "Paris", "Italie": "Rome", "Espagne": "Madrid", "Angleterre": "Londres", "Allemagne": "Berlin"}
            pays = random.choice(list(data.keys()))
            return f"Capitale de : {pays} ?", data[pays]
        
        elif self.type == 1: # Maths
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            op = random.choice(["+", "-", "*"])
            if op == "+": res = a + b
            elif op == "-": res = a - b
            else: res = a * b
            return f"Calcule : {a} {op} {b} =", str(res)
        
        elif self.type == 2: # Code mémoire
            code = str(random.randint(1000, 9999))
            return "Retiens et tape ce code :", code

    def handle_event(self, event):
        """Gère la saisie clavier. Retourne True si gagné, False si perdu, None si en cours."""
        if event.type == pygame.KEYDOWN:
            
            # Effacer
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            
            # Valider
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip().lower() == self.reponse.lower():
                    return True # GAGNÉ
                else:
                    self.input_text = "" # Reset champ
                    return False # PERDU
            
            # Écrire
            else:
                # Limite à 10 caractères
                if len(self.input_text) < 10:
                    self.input_text += event.unicode
        return None

    def draw(self, screen):
        # Fond sombre pour l'énigme
        screen.fill((20, 30, 40))
        
        # Titre
        titre = self.font_big.render("ÉNIGME", True, (255, 215, 0))
        screen.blit(titre, (screen.get_width()//2 - titre.get_width()//2, 100))

        # Question
        lbl_q = self.font.render(self.question, True, (255, 255, 255))
        screen.blit(lbl_q, (screen.get_width()//2 - lbl_q.get_width()//2, 250))
        
        # Indice pour le code (si type 2)
        if self.type == 2:
            indice = self.font.render(f"(Code: {self.reponse})", True, (100, 100, 100))
            screen.blit(indice, (screen.get_width()//2 - indice.get_width()//2, 300))

        # Champ de réponse (Rectangle)
        input_box = pygame.Rect(screen.get_width()//2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        
        # Texte tapé
        txt_surface = self.font.render(self.input_text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        
        # Instruction
        info = pygame.font.Font(None, 24).render("Écris ta réponse et appuie sur ENTRÉE", True, (150, 150, 150))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 460))