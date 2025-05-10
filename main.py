import pygame, sys
from pygame.locals import *
import random as rd
import time

from game.modules.entities import Enemy
from modules.player import Player


pygame.init()


# ========== Define constants ========== #

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants
SCREEN_SHAPE = (600, 800)
TIME_UNTIL_QUICKER = 4000
TIME_BEFORE_ENEMY_MOVE = 500
TIME_BEFORE_NEW_ENEMY = 2000
PLAYER_MOVING_SPEED = 10
ENEMY_MOVING_SPEED = 100
ENEMY_WIDTH = 100
PLAYER_WIDTH = 60
PLAYER_IMAGE_PATH = "multimedia/toto.png"
ENEMY_IMAGE_PATHS = [
    "multimedia/requin.png",
    "multimedia/requin2.png",
    "multimedia/requin3.png",
]

# Variables
score = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

DISPLAYSURF = pygame.display.set_mode(SCREEN_SHAPE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

P1 = Player(SCREEN_SHAPE, PLAYER_IMAGE_PATH, PLAYER_WIDTH, PLAYER_MOVING_SPEED)


# ========== Load variables ========== #

# Images & music
# background = pygame.image.load("multimedia/AnimatedStreet.png")
pygame.mixer.music.load("multimedia/shark-is-near.mp3")
pygame.mixer.music.play(-1)

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemy_centers = []
for i in range(1):
    enemy = Enemy(
        enemy_centers,
        SCREEN_SHAPE,
        ENEMY_IMAGE_PATHS,
        ENEMY_WIDTH,
        ENEMY_MOVING_SPEED,
    )
    enemies.add(enemy)
    enemy_centers.append(enemy.rect.center[0])
all_sprites = enemies.copy()
all_sprites.add(P1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, TIME_UNTIL_QUICKER)
ENEMY_MOVE = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_MOVE, TIME_BEFORE_ENEMY_MOVE)
NEW_ENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(NEW_ENEMY, TIME_BEFORE_NEW_ENEMY)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            for enemy in enemies:
                if enemy.speed < 20:
                    enemy.speed += 5

        if event.type == ENEMY_MOVE:
            for enemy in enemies:
                DISPLAYSURF.blit(enemy.image, enemy.rect)
                score = enemy.move(score)

        if event.type == NEW_ENEMY:
            enemy_centers = []
            enemy = Enemy(
                enemy_centers,
                SCREEN_SHAPE,
                ENEMY_IMAGE_PATHS,
                ENEMY_WIDTH,
                ENEMY_MOVING_SPEED,
            )
            enemy_centers.append(enemy.rect.center[0])
            enemies.add(enemy)
            all_sprites.add(enemy)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(BLUE)
    # DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render("Score: " + str(score), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if entity in enemies:
            continue
        entity.move()

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        # Sound
        pygame.mixer.music.stop()
        pygame.mixer.Sound("multimedia/dead.mp3").play()

        # Visual
        DISPLAYSURF.fill(BLUE)
        DISPLAYSURF.blit(
            game_over,
            (
                (SCREEN_SHAPE[0] - game_over.get_rect().width) / 2,
                min(250, SCREEN_SHAPE[1] / 2),
            ),
        )
        DISPLAYSURF.blit(
            scores,
            (
                (SCREEN_SHAPE[0] - game_over.get_rect().width) / 2,
                min(350, SCREEN_SHAPE[1] / 2),
            ),
        )
        pygame.display.update()

        # Entities
        for entity in all_sprites:
            entity.kill()

        time.sleep(5)
        pygame.quit()
        sys.exit()

    # # Draw hitboxes in black (1 = border thickness)
    # pygame.draw.rect(DISPLAYSURF, BLACK, P1.rect, 1)
    # for e in enemies:
    #     pygame.draw.rect(DISPLAYSURF, BLACK, e.rect, 1)

    pygame.display.update()
    FramePerSec.tick(FPS)
