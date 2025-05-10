import pygame
from pygame.locals import *
import random as rd


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        entity_centers: list,
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

        self.entity_centers = entity_centers
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
                for val in self.entity_centers
            )
        ]
        return (
            rd.choice(screen_possibilities),
            0,
        )

    def move(self, score: int):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > self.screen_shape[1]:
            self.kill()
            score += 1
        return score


class Wave(pygame.sprite.Sprite):
    def __init__(
        self,
        entity_centers: list,
        screen_shape: tuple,
        wave_image_path: list,
        wave_width: int,
        wave_moving_speed: int,
    ):
        super().__init__()
        self.screen_shape = screen_shape
        self.wave_image_path = wave_image_path
        self.wave_width = wave_width
        self.speed = wave_moving_speed

        self.entity_centers = entity_centers
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.rect.center = self._get_location()

    def _get_image(self):
        image = pygame.image.load(self.wave_image_path)
        image_width, image_height = image.get_size()
        return pygame.transform.scale(
            image, (self.wave_width, self.wave_width * image_height / image_width)
        )

    def _get_location(self):
        screen_possibilities = [
            integer
            for integer in range(
                self.image.get_width(), self.screen_shape[0] - self.image.get_width()
            )
            if all(
                (integer < val - self.wave_width / 2)
                or (integer > val + self.wave_width / 2)
                for val in self.entity_centers
            )
        ]
        return (
            # rd.randint(self.image.get_width(), SCREEN_WIDTH - self.image.get_width()),
            rd.choice(screen_possibilities),
            0,
        )

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > self.screen_shape[1]:
            self.kill()
