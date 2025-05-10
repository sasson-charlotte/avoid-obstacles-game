import pygame, sys
from pygame.locals import *
import pygame_widgets as pw
from pygame_widgets.button import Button
import random as rd
import time

from modules.entities import Enemy, Wave
from modules.player import Player

pygame.mixer.pre_init(44100, -16, 1, 512)
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

# === Constants === #
# Overall
SCREEN_SHAPE = (600, 800)
WAVE_PROBABILITY = 10 # %

# User events
TIME_UNTIL_QUICKER = 4000
TIME_BEFORE_ENEMY_MOVE = 500
TIME_BEFORE_NEW_ENEMY = 2000

# Speed
PLAYER_MOVING_SPEED = 10
ENEMY_MOVING_SPEED = 100
WAVE_MOVING_SPEED = 100

# Dimensions
ENEMY_WIDTH = 100
WAVE_WIDTH = 100
PLAYER_WIDTH = 60

# Image paths
PLAYER_IMAGE_PATH = "multimedia/toto.png"
WAVE_IMAGE_PATH = "multimedia/vague3.png"
ENEMY_IMAGE_PATHS = [
    "multimedia/requin.png",
    "multimedia/requin2.png",
    "multimedia/requin3.png",
]

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


# ========== Load variables ========== #

DISPLAYSURF = pygame.display.set_mode(SCREEN_SHAPE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

P1 = Player(SCREEN_SHAPE, PLAYER_IMAGE_PATH, PLAYER_WIDTH, PLAYER_MOVING_SPEED)

# Images & music
# background = pygame.image.load("multimedia/AnimatedStreet.png")
pygame.mixer.music.load("multimedia/shark-is-near.mp3")
dead_sound = pygame.mixer.Sound("multimedia/dead.mp3")
pygame.mixer.music.play(-1)

# Creating Sprites Groups
enemies = pygame.sprite.Group()
waves = pygame.sprite.Group()
entity_centers = []
for i in range(1):
    enemy = Enemy(
        entity_centers,
        SCREEN_SHAPE,
        ENEMY_IMAGE_PATHS,
        ENEMY_WIDTH,
        ENEMY_MOVING_SPEED,
    )
    enemies.add(enemy)
    entity_centers.append(enemy.rect.center[0])
all_sprites = enemies.copy()
all_sprites.add(P1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, TIME_UNTIL_QUICKER)
ENEMY_MOVE = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_MOVE, TIME_BEFORE_ENEMY_MOVE)
NEW_ENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(NEW_ENEMY, TIME_BEFORE_NEW_ENEMY)

# Type of screen
is_game_over = False
is_game_restarted = False
score = 0

def replay_game():
    global is_game_over, is_game_restarted, replay_button
    is_game_over = False
    is_game_restarted = True
    replay_button.hide()
    replay_button.disable()

while True:
    if is_game_over:
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

        # Button
        replay_button = Button(
            DISPLAYSURF,
            (SCREEN_SHAPE[0] - 200) / 2,
            min(800, SCREEN_SHAPE[1] / 2),
            200, 50,
            text='Replay',
            font=font_small,
            inactiveColour=(200, 200, 200),
            hoverColour=(150, 150, 150),
            pressedColour=(100, 100, 100),
            onClick=replay_game
        )

        # Entities
        for entity in all_sprites:
            entity.kill()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # time.sleep(5)
        pw.update(events)
        pygame.display.update()

    elif is_game_restarted:
        # Creating Sprites Groups
        enemies = pygame.sprite.Group()
        waves = pygame.sprite.Group()
        entity_centers = []
        for i in range(1):
            enemy = Enemy(
                entity_centers,
                SCREEN_SHAPE,
                ENEMY_IMAGE_PATHS,
                ENEMY_WIDTH,
                ENEMY_MOVING_SPEED,
            )
            enemies.add(enemy)
            entity_centers.append(enemy.rect.center[0])
        all_sprites = enemies.copy()
        all_sprites.add(P1)

        is_game_restarted = False
        score = 0

    else:
        events = pygame.event.get()
        for event in events:
            if event.type == INC_SPEED:
                if TIME_BEFORE_NEW_ENEMY > 1000:
                    TIME_BEFORE_NEW_ENEMY -= 500
                    pygame.time.set_timer(NEW_ENEMY, TIME_BEFORE_NEW_ENEMY)

            if event.type == ENEMY_MOVE:
                for entity in list(enemies) + list(waves):
                    DISPLAYSURF.blit(entity.image, entity.rect)
                    if entity in enemies:
                        score = entity.move(score)
                    else:
                        entity.move()

            if event.type == NEW_ENEMY:
                entity_centers = []
                is_enemy = rd.choice(range(1, 101))
                if is_enemy < WAVE_PROBABILITY:
                    wave = Wave(
                        entity_centers,
                        SCREEN_SHAPE,
                        WAVE_IMAGE_PATH,
                        WAVE_WIDTH,
                        WAVE_MOVING_SPEED,
                    )
                    entity_centers.append(wave.rect.center[0])
                    waves.add(wave)
                    all_sprites.add(wave)
                else:
                    enemy = Enemy(
                        entity_centers,
                        SCREEN_SHAPE,
                        ENEMY_IMAGE_PATHS,
                        ENEMY_WIDTH,
                        ENEMY_MOVING_SPEED,
                    )
                    entity_centers.append(enemy.rect.center[0])
                    enemies.add(enemy)
                    all_sprites.add(enemy)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Move and Re-draw all Sprites
        DISPLAYSURF.fill(BLUE)
        # DISPLAYSURF.blit(background, (0, 0))
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            if entity in enemies or entity in waves:
                continue
            entity.move()

        # If player surfs a wave
        taken_wave = pygame.sprite.spritecollideany(P1, waves)
        if taken_wave:
            pygame.mixer.music.pause()
            pygame.mixer.Sound("multimedia/success.ogg").play()
            pygame.mixer.music.unpause()
            taken_wave.kill()

            score += 20

        # If player is eaten
        if pygame.sprite.spritecollideany(P1, enemies):
            is_game_over = True

            # Sound
            pygame.mixer.music.stop()
            dead_sound.play()

        scores = font_small.render("Score: " + str(score), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        # # Draw hitboxes in black (1 = border thickness)
        # pygame.draw.rect(DISPLAYSURF, BLACK, P1.rect, 1)
        # for e in enemies:
        #     pygame.draw.rect(DISPLAYSURF, BLACK, e.rect, 1)

        pw.update(events)
        pygame.display.update()
        FramePerSec.tick(FPS)
