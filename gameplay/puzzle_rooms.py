import pygame
import random
import unicodedata


class PuzzleRoom:
    def __init__(self):
        # 0 = Géo, 1 = Math, 2 = Code mémoire
        self.type = random.randint(0, 2)

        self.question = ""
        self.reponse = ""
        self.instruction = ""
        self.max_input_len = 12

        self.generer_enigme()

        self.input_text = ""
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 28)

        # Affichage temporaire du code mémoire
        self.creation_time = pygame.time.get_ticks()
        self.code_visible_duration_ms = 2500

    def generer_enigme(self):
        """
        Initialise l'énigme courante selon son type.
        """
        if self.type == 0:
            # Géographie
            data = {
                "France": "Paris",
                "Italie": "Rome",
                "Espagne": "Madrid",
                "Angleterre": "Londres",
                "Allemagne": "Berlin"
            }
            pays = random.choice(list(data.keys()))
            self.question = f"Capitale de : {pays} ?"
            self.reponse = data[pays]
            self.instruction = "Écris la capitale puis appuie sur ENTRÉE"
            self.max_input_len = 20

        elif self.type == 1:
            # Maths
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            op = random.choice(["+", "-", "*"])

            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            else:
                res = a * b

            self.question = f"Calcule : {a} {op} {b} ="
            self.reponse = str(res)
            self.instruction = "Écris le résultat puis appuie sur ENTRÉE"
            self.max_input_len = 10

        else:
            # Code mémoire
            code = str(random.randint(1000, 9999))
            self.question = "Retiens ce code puis retape-le"
            self.reponse = code
            self.instruction = "Le code disparaît rapidement. Retape-le puis ENTRÉE"
            self.max_input_len = 10

    def _normalize_text(self, text):
        """
        Normalise un texte pour comparer les réponses plus proprement :
        - retire espaces en trop
        - ignore majuscules/minuscules
        - simplifie les accents
        """
        text = text.strip().lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        return text

    def _is_correct_answer(self):
        user_answer = self._normalize_text(self.input_text)
        correct_answer = self._normalize_text(self.reponse)
        return user_answer == correct_answer

    def handle_event(self, event):
        """
        Gère la saisie clavier.
        Retourne :
        - True si gagné
        - False si perdu
        - None si en cours
        """
        if event.type == pygame.KEYDOWN:

            # Effacer
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

            # Valider
            elif event.key == pygame.K_RETURN:
                if self._is_correct_answer():
                    return True
                else:
                    self.input_text = ""
                    return False

            # Écrire
            else:
                if event.unicode.isprintable() and len(self.input_text) < self.max_input_len:
                    self.input_text += event.unicode

        return None

    def draw(self, screen):
        screen.fill((20, 30, 40))

        # Titre
        titre = self.font_big.render("ÉNIGME", True, (255, 215, 0))
        screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, 80))

        # Question
        lbl_q = self.font.render(self.question, True, (255, 255, 255))
        screen.blit(lbl_q, (screen.get_width() // 2 - lbl_q.get_width() // 2, 200))

        # Cas spécial : code mémoire
        if self.type == 2:
            elapsed = pygame.time.get_ticks() - self.creation_time

            if elapsed <= self.code_visible_duration_ms:
                indice = self.font.render(f"CODE : {self.reponse}", True, (255, 255, 255))
            else:
                indice = self.font.render("CODE MASQUÉ", True, (120, 120, 120))

            screen.blit(indice, (screen.get_width() // 2 - indice.get_width() // 2, 260))

        # Champ de réponse
        input_box = pygame.Rect(screen.get_width() // 2 - 160, 380, 320, 55)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        txt_surface = self.font.render(self.input_text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 12, input_box.y + 10))

        # Instruction
        info = self.font_small.render(self.instruction, True, (170, 170, 170))
        screen.blit(info, (screen.get_width() // 2 - info.get_width() // 2, 455))