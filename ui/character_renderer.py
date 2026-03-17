import pygame


def _clamp_color(value):
    return max(0, min(255, int(value)))


def lighten_color(color, amount=30):
    r, g, b = color
    return (
        _clamp_color(r + amount),
        _clamp_color(g + amount),
        _clamp_color(b + amount),
    )


def darken_color(color, amount=30):
    r, g, b = color
    return (
        _clamp_color(r - amount),
        _clamp_color(g - amount),
        _clamp_color(b - amount),
    )


def draw_adventurer(surface, x, y, width, height, color, facing_right=True, actif=False):
    """
    Dessine un personnage style aventurier mignon.
    x, y = coin haut gauche.
    """
    base_color = color
    light_color = lighten_color(base_color, 35)
    dark_color = darken_color(base_color, 45)

    outline = (255, 255, 255)
    soft_outline = (25, 25, 30)
    skin = (245, 220, 190)
    eye_white = (255, 255, 255)
    eye_pupil = (35, 35, 35)
    belt_color = (101, 67, 33)
    bag_color = (120, 82, 45)
    hat_color = (88, 58, 35)
    scarf_color = (210, 170, 70)

    # Ombre au sol
    shadow_rect = pygame.Rect(x - 2, y + height - 6, width + 8, 14)
    pygame.draw.ellipse(surface, (0, 0, 0), shadow_rect)

    # Sac à dos
    bag_w = int(width * 0.22)
    bag_h = int(height * 0.38)
    bag_x = x - bag_w // 2 if facing_right else x + width - bag_w // 2
    bag_y = y + int(height * 0.34)

    bag_rect = pygame.Rect(bag_x, bag_y, bag_w, bag_h)
    pygame.draw.rect(surface, bag_color, bag_rect, border_radius=6)
    pygame.draw.rect(surface, soft_outline, bag_rect, 2, border_radius=6)

    # Corps
    body_rect = pygame.Rect(x, y + int(height * 0.20), width, int(height * 0.72))
    pygame.draw.rect(surface, base_color, body_rect, border_radius=14)
    pygame.draw.rect(surface, soft_outline, body_rect, 2, border_radius=14)

    # Tête
    head_w = int(width * 0.82)
    head_h = int(height * 0.36)
    head_x = x + (width - head_w) // 2
    head_y = y
    head_rect = pygame.Rect(head_x, head_y, head_w, head_h)
    pygame.draw.ellipse(surface, skin, head_rect)
    pygame.draw.ellipse(surface, soft_outline, head_rect, 2)

    # Chapeau / cheveux
    hat_rect = pygame.Rect(head_x - 2, head_y - 2, head_w + 4, int(head_h * 0.52))
    pygame.draw.ellipse(surface, hat_color, hat_rect)
    pygame.draw.ellipse(surface, soft_outline, hat_rect, 2)

    hat_band = pygame.Rect(
        head_x + int(head_w * 0.18),
        head_y + int(head_h * 0.16),
        int(head_w * 0.64),
        int(head_h * 0.12)
    )
    pygame.draw.rect(surface, scarf_color, hat_band, border_radius=4)

    # Foulard
    scarf_rect = pygame.Rect(
        x + int(width * 0.18),
        y + int(height * 0.29),
        int(width * 0.64),
        int(height * 0.10)
    )
    pygame.draw.rect(surface, scarf_color, scarf_rect, border_radius=5)
    pygame.draw.rect(surface, soft_outline, scarf_rect, 1, border_radius=5)

    # Reflet sur le corps
    shine_rect = pygame.Rect(
        x + int(width * 0.12),
        y + int(height * 0.28),
        int(width * 0.22),
        int(height * 0.45)
    )
    pygame.draw.rect(surface, light_color, shine_rect, border_radius=10)

    # Ceinture
    belt_rect = pygame.Rect(
        x + int(width * 0.12),
        y + int(height * 0.58),
        int(width * 0.76),
        int(height * 0.09)
    )
    pygame.draw.rect(surface, belt_color, belt_rect, border_radius=4)
    pygame.draw.rect(surface, soft_outline, belt_rect, 1, border_radius=4)

    buckle_rect = pygame.Rect(
        x + int(width * 0.42),
        y + int(height * 0.585),
        int(width * 0.16),
        int(height * 0.07)
    )
    pygame.draw.rect(surface, (210, 180, 80), buckle_rect, border_radius=3)
    pygame.draw.rect(surface, soft_outline, buckle_rect, 1, border_radius=3)

    # Bras
    arm_w = int(width * 0.18)
    arm_h = int(height * 0.34)
    left_arm = pygame.Rect(x - int(width * 0.06), y + int(height * 0.36), arm_w, arm_h)
    right_arm = pygame.Rect(x + width - arm_w + int(width * 0.06), y + int(height * 0.36), arm_w, arm_h)

    pygame.draw.rect(surface, dark_color, left_arm, border_radius=8)
    pygame.draw.rect(surface, dark_color, right_arm, border_radius=8)
    pygame.draw.rect(surface, soft_outline, left_arm, 2, border_radius=8)
    pygame.draw.rect(surface, soft_outline, right_arm, 2, border_radius=8)

    # Jambes
    leg_w = int(width * 0.24)
    leg_h = int(height * 0.23)
    leg_gap = int(width * 0.10)

    left_leg = pygame.Rect(x + int(width * 0.18), y + height - leg_h, leg_w, leg_h)
    right_leg = pygame.Rect(x + int(width * 0.18) + leg_w + leg_gap, y + height - leg_h, leg_w, leg_h)

    pygame.draw.rect(surface, dark_color, left_leg, border_radius=8)
    pygame.draw.rect(surface, dark_color, right_leg, border_radius=8)
    pygame.draw.rect(surface, soft_outline, left_leg, 2, border_radius=8)
    pygame.draw.rect(surface, soft_outline, right_leg, 2, border_radius=8)

    # Yeux
    eye_y = head_y + int(head_h * 0.43)
    eye_w = max(6, int(width * 0.13))
    eye_h = max(10, int(height * 0.16))

    if facing_right:
        left_eye_x = head_x + int(head_w * 0.30)
        right_eye_x = head_x + int(head_w * 0.56)
    else:
        left_eye_x = head_x + int(head_w * 0.26)
        right_eye_x = head_x + int(head_w * 0.52)

    left_eye = pygame.Rect(left_eye_x, eye_y, eye_w, eye_h)
    right_eye = pygame.Rect(right_eye_x, eye_y, eye_w, eye_h)

    pygame.draw.ellipse(surface, eye_white, left_eye)
    pygame.draw.ellipse(surface, eye_white, right_eye)
    pygame.draw.ellipse(surface, soft_outline, left_eye, 1)
    pygame.draw.ellipse(surface, soft_outline, right_eye, 1)

    pupil_offset = 2 if facing_right else -1
    left_pupil = pygame.Rect(left_eye.x + eye_w // 2 - 2 + pupil_offset, left_eye.y + 4, 4, 6)
    right_pupil = pygame.Rect(right_eye.x + eye_w // 2 - 2 + pupil_offset, right_eye.y + 4, 4, 6)

    pygame.draw.ellipse(surface, eye_pupil, left_pupil)
    pygame.draw.ellipse(surface, eye_pupil, right_pupil)

    pygame.draw.circle(surface, (255, 255, 255), (left_eye.x + 2, left_eye.y + 3), 1)
    pygame.draw.circle(surface, (255, 255, 255), (right_eye.x + 2, right_eye.y + 3), 1)

    # Bouche
    mouth_y = head_y + int(head_h * 0.72)
    pygame.draw.arc(
        surface,
        (120, 70, 70),
        pygame.Rect(head_x + int(head_w * 0.38), mouth_y, int(head_w * 0.22), 8),
        0.2,
        2.9,
        1
    )

    # Contour actif
    if actif:
        pygame.draw.rect(surface, outline, body_rect.inflate(6, 6), 2, border_radius=16)