from __future__ import annotations

from abc import abstractmethod

from models.game.item import Item
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from models.internal.configs import MovableConfig


class Movable(Item):
    def __init__(self, x,y,width,height, color: tuple[int, int, int], speed: int):
        super().__init__(x,y,width,height, color)

        self.speed = speed

    @abstractmethod
    def move(self): ...

    def update(self):
        self.move()

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)

    
