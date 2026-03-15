import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lobby")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arial", 80, True)
player_font = pygame.font.SysFont("arial", 28)
info_font = pygame.font.SysFont("arial", 32)

players = ["A", "B", "C"]


def draw_background():

    screen.fill((8,10,15))

    # halo sombre derrière les portes
    pygame.draw.circle(screen,(30,30,35),(WIDTH//2,400),520)

    # lumière plafond
    pygame.draw.rect(screen,(50,50,60),(WIDTH//2 - 200,70,400,12),border_radius=6)


def draw_player_count():

    text = info_font.render(f"Players : {len(players)}", True, (255,255,255))
    screen.blit(text,(20,20))


def draw_doors():

    door_width = 180
    door_height = 300

    global door_positions

    door_positions = [
        WIDTH//2 - 360,
        WIDTH//2 - door_width//2,
        WIDTH//2 + 180
    ]

    door_colors = [
        (180,50,50),
        (50,100,220),
        (50,180,100)
    ]

    for i in range(3):

        x = door_positions[i]

        shadow = pygame.Rect(x+8,248,door_width,door_height)
        pygame.draw.rect(screen,(0,0,0),shadow,border_radius=12)

        door = pygame.Rect(x,240,door_width,door_height)
        pygame.draw.rect(screen,door_colors[i],door,border_radius=12)

        pygame.draw.rect(screen,(255,255,255),door,3,border_radius=12)


def draw_dice():

    size = 80

    dice_colors = [
        (200,60,60),
        (60,120,220),
        (60,200,120)
    ]

    for i in range(3):

        # centre du dé sous la porte
        x = door_positions[i] + 90 - size//2
        y = 580

        dice = pygame.Rect(x,y,size,size)

        pygame.draw.rect(screen,dice_colors[i],dice,border_radius=12)
        pygame.draw.rect(screen,(30,30,30),dice,3,border_radius=12)

        dots = [
            (x+20,y+20),
            (x+60,y+20),
            (x+20,y+60),
            (x+60,y+60),
            (x+40,y+40)
        ]

        for dot in dots:
            pygame.draw.circle(screen,(0,0,0),dot,6)


def draw_players():

    start_y = 540

    for i, player in enumerate(players):

        y = start_y + i*40

        name = player_font.render(player,True,(255,255,255))
        screen.blit(name,(80,y))

        for v in range(10):

            pygame.draw.circle(
                screen,
                (220,40,40),
                (120 + v*14, y + 14),
                6
            )


def draw_title():

    title = title_font.render("LOBBY",True,(255,255,255))
    screen.blit(title,(WIDTH//2 - title.get_width()//2,90))


def draw_lobby():

    draw_background()
    draw_player_count()
    draw_title()
    draw_doors()
    draw_dice()
    draw_players()


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    draw_lobby()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
