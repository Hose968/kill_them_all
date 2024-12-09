from __future__ import annotations

from abc import ABC, abstractmethod
from models.internal.configs import Shape
import pygame
from uuid import uuid4



class Item(ABC):
    def __init__(self, x,y, width, height, color: tuple[int, int, int]):
        self._id = str(uuid4())
        self._parent_id = None
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.rect = pygame.Rect(self.shape)
        self.color = color

    @abstractmethod
    def draw(self, surface: pygame.Surface): ...

    @abstractmethod
    def remove(self): ...

    @abstractmethod
    def update(self): ...

    @property
    def center(self):
        return self.rect.center

    @property
    def id(self):
        return self._id

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        self._parent_id = parent_id

    @property
    def shape(self):
        return (self.x, self.y, self.width, self.height)

    
    