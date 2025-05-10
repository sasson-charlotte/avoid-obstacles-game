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
