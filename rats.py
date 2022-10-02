from tkinter.tix import MAX
import os
import random
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RatSavers")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 205)


BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BLOOP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "bloop.wav"))
CRASH_SOUND = pygame.mixer.Sound(os.path.join("Assets", "crash.wav"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("conicsans", 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
RAFT_WIDTH, RAFT_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1

RAFT_IMAGE = pygame.image.load(os.path.join("Assets", "raft.png"))
DOCK_IMAGE = pygame.image.load(os.path.join("Assets", "dock.png"))
TRASH_IMAGE = pygame.image.load(os.path.join("Assets", "trash.png"))

RAFT_RECT = pygame.transform.rotate(
    pygame.transform.scale(RAFT_IMAGE, (RAFT_WIDTH, RAFT_HEIGHT)), 0
)

RAT_IMAGE = pygame.image.load(os.path.join("Assets", "rat.png"))


SEWER = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "sewer.png")), (WIDTH, HEIGHT)
)


def draw_gameover(saved_rat_count):
    draw_text = WINNER_FONT.render(
        f"Game Over, Saved {saved_rat_count} Rats", 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )

    pygame.display.update()
    pygame.time.delay(5000)


def draw_lost_rats(rat_count):
    draw_text = WINNER_FONT.render(f"Too Many Rats!", 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )

    pygame.display.update()
    pygame.time.delay(5000)


def draw_rats_saved(rat_count):
    draw_text = WINNER_FONT.render(f"Saved {rat_count} Rats!", 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )

    pygame.display.update()
    pygame.time.delay(1000)


# region waves
WAVE_LIST = []
MAX_WAVES = 10000


def update_wave_list():
    if MAX_WAVES >= len(WAVE_LIST):
        wave = create_wave()
        WAVE_LIST.append(wave)


def handle_wave_movement():
    for wave in WAVE_LIST:
        if wave.y >= HEIGHT:
            WAVE_LIST.remove(wave)
        else:
            wave.y += 3
        if wave.x > 10 and wave.x <= WIDTH - 70:
            if wave.x > WIDTH // 2:
                wave.x += random.randint(2, 5)
            if wave.x <= WIDTH // 2:
                wave.x -= random.randint(2, 5)


def create_wave():
    center = WIDTH // 2
    max_x = center + 30
    min_x = center - 30
    max_y = center
    min_y = center - 200

    wave_x = random.randrange(min_x, max_x)
    wave_y = random.randrange(min_y, max_y)
    wave = pygame.Rect(
        wave_x, wave_y, random.randrange(
            3, 5), random.randrange(
            5, 20))
    return wave

# endregion waves


# region rats
RAT_LIST = []
MAX_RATS = 3


def update_rat_list():
    if MAX_RATS > len(RAT_LIST):
        rat = create_rat()
        RAT_LIST.append(rat)


def handle_rat_movement():
    for rat in RAT_LIST:
        if rat.y >= HEIGHT:
            RAT_LIST.remove(rat)
            continue
        else:
            rat.y += 3
        if rat.x > 10 and rat.x <= WIDTH - 70:
            if rat.x > WIDTH // 2:
                rat.x += random.randint(2, 5)
            if rat.x <= WIDTH // 2:
                rat.x -= random.randint(2, 5)


def create_rat():
    center = WIDTH // 2
    max_x = center + 100
    min_x = center - 100
    max_y = HEIGHT // 2 - 1
    min_y = HEIGHT // 2 - 10

    rat_x = random.randrange(min_x, max_x)
    rat_y = random.randrange(min_y, max_y)
    rat = pygame.Rect(
        rat_x, rat_y, 25, 25)
    return rat

# endregion rats


# region trash
TRASH_LIST = []
MAX_TRASH = 1


def update_trash_list():
    if MAX_TRASH > len(TRASH_LIST):
        trash = create_trash()
        TRASH_LIST.append(trash)


def handle_trash_movement():
    for trash in TRASH_LIST:
        if trash.y >= HEIGHT:
            TRASH_LIST.remove(trash)
        else:
            trash.y += 3
        if trash.x > 10 and trash.x <= WIDTH - 70:
            if trash.x > WIDTH // 2:
                trash.x += random.randint(1, 3)
            if trash.x <= WIDTH // 2:
                trash.x -= random.randint(1, 3)


def create_trash():
    center = WIDTH // 2
    max_x = center + 100
    min_x = center - 100
    max_y = HEIGHT // 2 + 10
    min_y = HEIGHT // 2 + 1

    trash_x = random.randrange(min_x, max_x)
    trash_y = random.randrange(min_y, max_y)
    trash = pygame.Rect(
        trash_x,  trash_y, 50, 50)
    return trash

# endregion trash


# region docks
DOCK_LIST = []
MAX_DOCKS = 1
DOCK_CHECK = False
DOCK_PAUSE_COUNT = 0


def update_docks_list(rat_count):
    global DOCK_PAUSE_COUNT
    if MAX_DOCKS > len(DOCK_LIST) and rat_count >= 10 and DOCK_PAUSE_COUNT == 0:
        dock = create_dock()
        DOCK_LIST.append(dock)
    elif DOCK_PAUSE_COUNT > 0:
        DOCK_PAUSE_COUNT -= 1


def handle_dock_movement():
    global DOCK_CHECK
    global DOCK_PAUSE_COUNT
    for dock in DOCK_LIST:
        if dock.y >= HEIGHT:
            DOCK_LIST.remove(dock)
            DOCK_PAUSE_COUNT = 300
        if DOCK_CHECK == False:
            dock.y += 3
            if dock.x > HEIGHT//2:
                dock.x += random.randint(3, 5)
            DOCK_CHECK = True
        else:
            DOCK_CHECK = False


def handle_dock_movemensdfsdft():
    for dock in DOCK_LIST:
        if MAX_DOCKS == "False":
            if dock.y >= HEIGHT:
                DOCK_LIST.remove(dock)
            else:
                dock.y += 3
            if dock.x > HEIGHT//2:
                dock.x += random.randint(3, 5)
            DOCK_CHECK = True
        if DOCK_CHECK == True:
            DOCK_CHECK = False


def create_dock():
    # Right Dock
    dock_x = 450
    dock_y = 225

    # Left Dock
    # dock_x = 350
    # dock_y = 225

    dock = pygame.Rect(
        dock_x,  dock_y, 79, 63)
    return dock

# endregion docks


def draw_window(raft, rat_count, saved_count, raft_health):
    WIN.blit(SEWER, (0, 0))
    # pygame.draw.rect(WIN, BLACK, BORDER)

    rat_count_text = HEALTH_FONT.render("Rats: " + str(rat_count), 1, WHITE)
    saved_count_text = HEALTH_FONT.render(
        "Saved: " + str(saved_count), 1, WHITE)
    health_text = HEALTH_FONT.render("Health: " + str(raft_health), 1, WHITE)

    WIN.blit(rat_count_text, (WIDTH - rat_count_text.get_width() - 10, 10))
    saved_width = 40
    if saved_count >= 10:
        saved_width = 60
    WIN.blit(saved_count_text,
             (WIDTH - rat_count_text.get_width() - saved_width, 55))
    WIN.blit(health_text, (10, 10))

    # update_wave_list()
    # handle_wave_movement()

    handle_rat_movement()
    update_rat_list()

    handle_trash_movement()
    update_trash_list()

    handle_dock_movement()
    update_docks_list(rat_count)

    # Draw Waves
    for wave in WAVE_LIST:
        pygame.draw.rect(WIN, BLUE, wave)

    # Draw Trash

    # Draw Rats
    for rat in RAT_LIST:
        WIN.blit(RAT_IMAGE, (rat.x, rat.y))

    WIN.blit(RAFT_RECT, (raft.x, raft.y))

    for trash in TRASH_LIST:
        WIN.blit(TRASH_IMAGE, (trash.x, trash.y))

    for dock in DOCK_LIST:
        WIN.blit(DOCK_IMAGE, (dock.x, dock.y))

    # Add caught Rats to the raft
    if rat_count > 0:
        for i in range(rat_count):
            WIN.blit(RAT_IMAGE, (raft.x - RAFT_RECT.get_width() // 2 + random.randrange(
                0, 3), raft.y - RAFT_RECT.get_height() // 2 + random.randrange(0, 3)))

    pygame.display.update()


def handle_raft_movement(keys_pressed, raft):
    if keys_pressed[pygame.K_a] and raft.x - VEL > 60:  # Left
        raft.x -= VEL

    if keys_pressed[pygame.K_d] and raft.x + \
            VEL + raft.width < WIDTH - 60:  # Right
        raft.x += VEL

    if keys_pressed[pygame.K_w] and raft.y - VEL > HEIGHT - 100:  # Up
        raft.y -= VEL

    if (keys_pressed[pygame.K_s] and raft.y +
            VEL + raft.height < HEIGHT - 15):  # Down
        raft.y += VEL

def main():
    raft = pygame.Rect(100, HEIGHT - 100, RAFT_WIDTH, RAFT_HEIGHT)  # left

    rat_list = []
    rat_count = 0
    saved_count = 0
    raft_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if MAX_BULLETS >= len(rat_list):
                rat = pygame.Rect(
                    raft.x +
                    raft.width,
                    raft.y +
                    raft.height //
                    2 -
                    2,
                    10,
                    5)
                rat_list.append(rat)

            for rat in RAT_LIST:
                if raft.colliderect(rat):
                    BLOOP_SOUND.play()
                    rat_count += 1
                    RAT_LIST.remove(rat)

            for trash in TRASH_LIST:
                if raft.colliderect(trash):
                    CRASH_SOUND.play()
                    raft_health -= 1
                    TRASH_LIST.remove(trash)

            for dock in DOCK_LIST:
                if raft.colliderect(dock) and rat_count > 0:
                    saved_count = saved_count + rat_count
                    rat_count = 0
                    DOCK_LIST.remove(dock)

            if rat_count >= random.randrange(20, 25):
                draw_text = WINNER_FONT.render("Too Many Rats!", 1, WHITE)
                WIN.blit(
                    draw_text,
                    (
                        WIDTH / 2 - draw_text.get_width() / 2,
                        HEIGHT / 2 - draw_text.get_height() / 2,
                    ),
                )
                rat_count = 0

                pygame.display.update()
                pygame.time.delay(1000)

            if raft.x <= 65:
                raft_health -= 1

            if raft.x == WIDTH - 120:
                raft_health -= 1

        if raft_health <= 0:
            draw_gameover(saved_count)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_raft_movement(keys_pressed, raft)

        draw_window(raft, rat_count, saved_count, raft_health)

    main()


if __name__ == "__main__":
    main()
