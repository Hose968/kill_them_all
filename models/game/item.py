from __future__ import annotations

from abc import ABC, abstractmethod
import pygame
from uuid import uuid4
from models.internal.literals import RED



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

        self.remove_ready = False
        self.__max_health__ = 100
        self.__max_armor__ = 100

        self.health = 100
        self.armor = 0

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def remove(self, surface: pygame.Surface):
        pygame.draw.circle(surface, RED, self.center, self.rect.width // 2)

    def take_hits(self, bullets: list[Bullet]):
        for bullet in bullets:
            if not self.collideone(bullet):
                continue

            if bullet.parent_id == self.id:
                continue

            damage = bullet.damage
            bullet.remove_ready = True

            if self.armor > 0:
                armor_loss = min(damage // 2, self.armor)
                self.armor -= armor_loss
                damage -= armor_loss * 2

            self.health -= damage

            if self.health <= 0:
                self.remove_ready = True

    @abstractmethod
    def update(self, **kwargs): ...

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

    def collideone(self, item: Item):
        return self.rect.colliderect(item.rect)

    def collidemany(self, items: list[Item]):
        for index, item in enumerate(items):
            if self.collideone(item):
                return index

        return None

        

    
    