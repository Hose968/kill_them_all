from __future__ import annotations

from dataclasses import dataclass
import pygame
from models.internal.literals import WHITE, RED

@dataclass
class Config:
    pass

@dataclass
class GameConfig(Config):
    width: int = 1920
    height: int = 1080
    fps: int = 60

    # full_screen_flag: int = pygame.FULLSCREEN -- passed to display.set_mode as flag

    caption: str = "KillThemAll"

    # def __post_init__(self):
    #     self.width = max(self.width, 1280)
    #     self.height = max(self.height, 720)

    @property
    def screen_size(self):
        return (self.width, self.height)

    @property
    def center(self):
        return (self.width // 2, self.height // 2)

@dataclass
class Controls(Config):
    up: int
    down: int
    left: int
    right: int
    reborn: int
    shoot: int

@dataclass
class WASDControls(Controls):
    up: int = pygame.K_w
    down: int = pygame.K_s
    left: int = pygame.K_a
    right: int = pygame.K_d
    shoot: int = pygame.K_SPACE
    reborn: int = pygame.K_r

@dataclass
class ArrowsControls(Controls):
    up: int = pygame.K_UP
    down: int = pygame.K_DOWN
    left: int = pygame.K_LEFT
    right: int = pygame.K_RIGHT
    shoot: int = pygame.K_RCTRL
    reborn: int = pygame.K_RALT
