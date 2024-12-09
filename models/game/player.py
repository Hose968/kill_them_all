from __future__ import annotations

from models.game.movable import Movable

from models.internal.configs import Shape, Controls
from models.internal.literals import RED
from models.game.bullet import Bullet

from typing import Literal, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from models.game.block import Block


class Player(Movable):
    def __init__(
        self, 
        x,y,
        color: tuple[int, int, int],
        controls: Controls
    ):  
        super().__init__(x,y,26,40, color, 5)

        self.controls = controls

        self.health = 100
        self._max_health = 100

        self.armor = 0
        self._max_armor = 100

        self.score = 0

        self.starting_position = (x, y)
        self.is_alive = True
        self.direction: tuple[bool, bool, bool, bool] = (False, True, False, False) # up, down, left, right

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

    def update(self, surface: pygame.Surface, blocks: list[Block], bullets: list[Bullet], keys: list[bool]) -> list[Bullet]:
        self.reborn(keys)

        if self.is_alive == False:
            return bullets

        self.take_hits(bullets)

        if self.health <= 0:
            self.remove(surface)
        else:
            self.move(blocks, keys)
            bullets = bullets.append(self.shoot(keys))
            self.draw(surface)

        return bullets

    def move(self, blocks: list[Block], keys: list[bool]):
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        y_next_up = y + self.speed
        y_next_down = y - self.speed
        x_next_left = x - self.speed
        x_next_right = x + self.speed

        left_rect = pygame.Rect(x_next_left, y, width, height)
        right_rect = pygame.Rect(x_next_right, y, width, height)
        up_rect = pygame.Rect(x, y_next_up, width, height)
        down_rect = pygame.Rect(x, y_next_down, width, height)

        # collision with blocks
        for block in blocks:
            # left
            if block.rect.colliderect(left_rect):
                # move right
                self.rect.x += self.speed
            # right
            if block.rect.colliderect(right_rect):
                # move left
                self.rect.x -= self.speed
            # up
            if block.rect.colliderect(up_rect):
                # move down
                self.rect.y -= self.speed
            # down
            if block.rect.colliderect(down_rect):
                # move up
                self.rect.y += self.speed

        if keys[self.controls.up]:
            self.rect.y -= self.speed
            self.direction = (True, False, False, False)
        if keys[self.controls.down]:
            self.rect.y += self.speed
            self.direction = (False, True, False, False)
        if keys[self.controls.left]:
            self.rect.x -= self.speed
            self.direction = (False, False, True, False)
        if keys[self.controls.right]:
            self.rect.x += self.speed
            self.direction = (False, False, False, True)

    def remove(self, surface: pygame.Surface):
        self.is_alive = False
        pygame.draw.circle(surface, RED, self.rect.center, self.rect.width // 2)

    def reborn(self, keys: list[bool]):

        if not keys[self.controls.reborn]:
            return

        self.is_alive = True
        self.rect.x, self.rect.y = self.starting_position

        self.health = self._max_health
        self.armor = 0

        self.score = 0

        self.speed = 5

    def shoot(self, keys: list[bool]) -> list[Bullet]:
        if not keys[self.controls.shoot]:
            return []

        direction: tuple[int, int] = (0, -1) # x, y 

        if self.direction[0]:
            direction = (0, -1)
        elif self.direction[1]:
            direction = (0, 1)
        elif self.direction[2]:
            direction = (-1, 0)
        elif self.direction[3]:
            direction = (1, 0)

        bullet = Bullet(
            self.rect.x + self.rect.width // 2,
            self.rect.y + self.rect.height // 2,
            direction,
            self.color
        )

        bullet.parent_id = self.id
        
        return [bullet]

    def take_hits(self,surface: pygame.Surface, bullets: list[Bullet]):
        for bullet in bullets:

            if not self.rect.colliderect(bullet.rect):
                continue
            if bullet.parent_id == self.id:
                continue

            self.health -= bullet.damage
            if self.health <= 0:
                self.is_alive = False
            bullet.remove(surface=surface)
