from __future__ import annotations

from models.game.immovable import Immovable
from models.internal.literals import WHITE

class Block(Immovable):
    def __init__(self,x,y, width, height, color = WHITE):
        super().__init__(x,y,width, height, color)

    def update(self, bullets: list[Bullet]):
        for bullet in bullets:
            if self.collideone(bullet):
                bullet.remove_ready = True

