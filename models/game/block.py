from __future__ import annotations

from models.game.immovable import Immovable
from models.internal.configs import Shape, BlockConfig
from models.internal.literals import WHITE

class Block(Immovable):
    def __init__(self,x,y, width, height, color = WHITE):
        super().__init__(x,y,width, height, color)

    def remove(self):
        pass

    def update(self, surface: pygame.Surface):
        self.draw(surface)

