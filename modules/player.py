import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        screen_shape: tuple,
        player_image_path: str,
        player_width: int,
        player_moving_speed: int,
    ):
        super().__init__()
        self.screen_shape = screen_shape
        self.player_image_path = player_image_path
        self.player_width = player_width
        self.player_moving_speed = player_moving_speed

        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_shape[0] // 2, screen_shape[1] - 80)

    def _get_image(self):
        image = pygame.image.load(self.player_image_path)
        image_width, image_height = image.get_size()
        return pygame.transform.scale(
            image, (self.player_width, self.player_width * image_height / image_width)
        )

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > self.player_moving_speed:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.player_moving_speed, 0)
        if self.rect.right < self.screen_shape[0] - self.player_moving_speed:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.player_moving_speed, 0)
