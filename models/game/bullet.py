from __future__ import annotations

import pygame

import time

from models.game.movable import Movable
from models.game.block import Block
from models.internal.literals import GRAY

class Bullet(Movable):
    def __init__(self, x,y, direction: tuple[int, int], color: tuple[int, int, int], damage: int = 25):
        super().__init__(x,y,15,15, color, 25)

        self.direction = direction
        self.damage = damage

        self._birth = time.time()
        self.remove_ready = False

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
    
    def update(self, surface: pygame.Surface):
        self.move()

        if time.time() - self._birth > 1:
            self.remove_ready = True
        
        self.draw(surface)

    def remove(self, surface: pygame.Surface = None):
        pygame.draw.circle(surface, GRAY, self.rect.center, self.rect.width // 2)
        pygame.display.flip()