from __future__ import annotations

from models.game.movable import Movable

from models.internal.configs import Controls
from models.internal.literals import RED, BLUE
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
        controls: Controls,
        health: int = 100,
        armor: int = 0
    ):  
        super().__init__(x,y,26,40, color, 5)

        self.controls = controls

        self.score = 0

        self.shoot_pressed = False

        self.health = health
        self.armor = armor

        self.starting_position = (x, y)
        self.direction: tuple[bool, bool, bool, bool] = (False, True, False, False) # up, down, left, right

    @property
    def is_dead(self):
        return self.remove_ready

    @is_dead.setter
    def is_dead(self, value):
        self.remove_ready = value

    def update(self, bullets: list[Bullet], keys: list[bool]):
        self.reborn(keys)
        self.take_hits(bullets)

    def draw(self, surface: pygame.Surface):
        # Draw hitbar above the player rectangle
        hitbar_height = 5
        hitbar_padding = 2
        health_ratio = self.health / self.__max_health__
        hitbar_width = int(self.rect.width * health_ratio)
        
        # Define the hitbar rectangle
        hitbar_rect = pygame.Rect(
            self.rect.x, 
            self.rect.y - hitbar_height - hitbar_padding, 
            hitbar_width, 
            hitbar_height
        )
        
        # Draw armor bar above the hitbar
        armorbar_height = 5
        armorbar_padding = 2
        armor_ratio = self.armor / self.__max_armor__
        armorbar_width = int(self.rect.width * armor_ratio)
        
        # Define the armorbar rectangle
        armorbar_rect = pygame.Rect(
            self.rect.x, 
            self.rect.y - hitbar_height - armorbar_height - hitbar_padding - armorbar_padding, 
            armorbar_width, 
            armorbar_height
        )
        

        # Draw the hitbar
        pygame.draw.rect(surface, RED, hitbar_rect)
        # Draw the armorbar
        pygame.draw.rect(surface, BLUE, armorbar_rect)

        # Draw the player rectangle
        super().draw(surface)

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

    def reborn(self, keys: list[bool]):

        if not keys[self.controls.reborn]:
            return

        self.is_dead = False
        self.rect.x, self.rect.y = self.starting_position

        self.health = self.__max_health__
        self.armor = 0

        self.score = 0

        self.speed = 5

    def shoot(self, keys: list[bool]) -> list[Bullet]:
        if not keys[self.controls.shoot]:
            self.shoot_pressed = False
            return []

        if self.shoot_pressed:
            return []

        self.shoot_pressed = True

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
