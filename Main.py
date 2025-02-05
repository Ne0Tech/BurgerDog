import random, pygame

from pygame.examples.grid import WINDOW_WIDTH

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Burger Dog')

FPS = 60
clock = pygame.time.Clock()

PLAYER_STARTING_LIVES =3
PLAYER_NORMAL_VELOCITY =5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL =100
STARTING_BURGER_VELOCITY =3
BURGER_ACCELERATION =0.5
BUFFER_DISTANCE = 100


score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
starting_boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY


ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font("WashYourHand.ttf", 32)

def prep_text(text : str, background_color : tuple[int, int, int], **locations):
    text_to_return = font.render(text, True, background_color)
    rect = text_to_return.get_rect()
    for location in locations:

        if location == "topleft":
            rect.topleft = locations["topleft"]
        elif location == "centerx":
            rect.centerx = locations["centerx"]
       


    return (text_to_return, rect)
