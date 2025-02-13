import random, pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100

PLAYER_LIVES = PLAYER_STARTING_LIVES
BOOST_LEVEL = STARTING_BOOST_LEVEL
burger_points = 0
score = 0
burgers_eaten = 0
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = BOOST_LEVEL

STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

burger_velocity = STARTING_BURGER_VELOCITY

ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

font = pygame.font.Font("WashYourHand.ttf", 32)


def prep_text(text: str, background_color: tuple[int, int, int], **locations):
    text_to_return = font.render(text, True, background_color)
    rect = text_to_return.get_rect()

    for location in locations:
        if location == "topleft":
            rect.topleft = locations["topleft"]
        elif location == "centerx":
            rect.centerx = locations["centerx"]
        elif location == "y":
            rect.y = locations["y"]
        elif location == "topright":
            rect.topright = locations["topright"]
        elif location == "center":
            rect.center = locations["center"]

    return text_to_return, rect

player_image_right = pygame.image.load("dog_right.png")
player_image_left = pygame.image.load("dog_left.png")

player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT

points_text, points_rect = prep_text(f"Burger Points: {burger_points}", ORANGE, topleft=(10, 10))
score_text, score_rect = prep_text(f"Score: {score}", ORANGE, topleft=(10, 50))
title_text, title_rect = prep_text("Burger Dog", ORANGE, centerx=WINDOW_WIDTH // 2, y=10)
eaten_text, eaten_rect = prep_text(f"Burgers Eaten: {burgers_eaten}", ORANGE, centerx=WINDOW_WIDTH // 2, y=50)
lives_text, lives_rect = prep_text(f"Lives: {PLAYER_LIVES}", ORANGE, topright=(WINDOW_WIDTH - 10, 10))
boost_text, boost_rect = prep_text(f"Boost: {BOOST_LEVEL}", ORANGE, topright=(WINDOW_WIDTH - 10, 50))
game_over_text, game_over_rect = prep_text(f"FINAL SCORE: {score}", ORANGE,
                                           center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
continue_text, continue_rect = prep_text("Press any key to play again", ORANGE,
                                         center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64))

bark_sound = pygame.mixer.Sound("bark_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("bd_background_music.wav")

player_image_right = pygame.image.load("dog_right.png")
player_image_left = pygame.image.load("dog_left.png")
player_image = player_image_left

burger_image = pygame.image.load("burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)


def move_player(player_rect):
    global player_image
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left

    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_image = player_image_right

    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity

    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    engage_boost(keys)


def engage_boost(keys):
    global player_velocity, boost_level
    if keys[pygame.K_SPACE] and boost_level > 0:
        boost_level -= 1
        player_velocity = PLAYER_BOOST_VELOCITY
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY


def check_collisions(player_rect):
    global burger_points, score, burgers_eaten, burger_velocity, boost_level
    if player_rect.colliderect(burger_rect):
        burger_points += int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))
        score += burger_points
        burgers_eaten += 1
        bark_sound.play()
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION
        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL
def check_game_over():
    global game_over_text, is_paused, score, burgers_eaten, player_lives, boost_level, burger_velocity, running
    if player_lives == 0:
        game_over_text = font.render(f"FINAL SCORE: {score}", True, ORANGE)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    burgers_eaten = 0
                    player_lives = PLAYER_STARTING_LIVES
                    boost_level = STARTING_BOOST_LEVEL
                    burger_velocity = STARTING_BURGER_VELOCITY
                    pygame.mixer.music.play()
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
def update_hud():
    points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
    score_text = font.render("Score: " + str(score), True, ORANGE)
    eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
    lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
    boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)

def display_hud():
    display_surface.fill(BLACK)
    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
     pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOW_WIDTH, 100), 3)
display_surface.blit(player_image, player_rect)
    # TODO (2025-02-10): blit player_image, player_rect
    # TODO (2025-02-10): blit burger_image, burger_rect
    pass  # TODO: (2025-02-10):  remove this when done.

def handle_clock():
    pygame.display.update()
    clock.tick(FPS)

while running:
    check_quit()
    move_player()
    move_burger()
    handle_miss()
    check_collisions()
    update_hud()
    display_hud()
    check_game_over()
    handle_clock()
pygame.quit()
