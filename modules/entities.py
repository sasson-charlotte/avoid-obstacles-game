import pygame
from pygame.locals import *
import random as rd


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        enemy_centers: list,
        screen_shape: tuple,
        enemy_image_paths: list,
        enemy_width: int,
        enemy_moving_speed: int,
    ):
        super().__init__()
        self.screen_shape = screen_shape
        self.enemy_image_paths = enemy_image_paths
        self.enemy_width = enemy_width
        self.speed = enemy_moving_speed

        self.enemy_centers = enemy_centers
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.rect.center = self._get_location()

    def _get_image(self):
        image = pygame.image.load(rd.choice(self.enemy_image_paths))
        image_width, image_height = image.get_size()
        return pygame.transform.scale(
            image, (self.enemy_width, self.enemy_width * image_height / image_width)
        )

    def _get_location(self):
        screen_possibilities = [
            integer
            for integer in range(
                self.image.get_width(), self.screen_shape[0] - self.image.get_width()
            )
            if all(
                (integer < val - self.enemy_width / 2)
                or (integer > val + self.enemy_width / 2)
                for val in self.enemy_centers
            )
        ]
        return (
            # rd.randint(self.image.get_width(), SCREEN_WIDTH - self.image.get_width()),
            rd.choice(screen_possibilities),
            0,
        )

    def move(self, score: int):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > self.screen_shape[1]:
            self.image = self._get_image()
            self.rect = self.image.get_rect()
            self.rect.top = 0
            self.rect.center = (
                rd.randint(
                    self.image.get_width(),
                    self.screen_shape[0] - self.image.get_width(),
                ),
                0,
            )
            score += 1
        return score
