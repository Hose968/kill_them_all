from __future__ import annotations

from models.game.item import Item
from models.internal.configs import Shape
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from models.internal.configs import ImmovableConfig


class Immovable(Item):
    def __init__(self, x,y,width,height, color: tuple[int, int, int]):
        super().__init__(x,y,width,height, color)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)