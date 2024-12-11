from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from models.internal.configs import GameConfig, WASDControls, ArrowsControls

from models.game.player import Player
from models.game.block import Block
from models.game.bullet import Bullet

from models.internal.literals import BLUE, GREEN, BLACK

if TYPE_CHECKING:
    from models.game.item import Item

class Game:
    def __init__(self, configs: GameConfig = GameConfig()):
        self.configs = configs

        pygame.display.set_caption(self.configs.caption)
        self.screen = pygame.display.set_mode(self.configs.screen_size)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.load_data()
        self.create_objects()

    def load_data(self):
        # here downloads any sounds, sprites, areas
        pass

    def create_objects(self):
        # here creates any objects: players, items, maps, enemies
        self.players: list[Player] = [
            Player(
                100, 100,
                BLUE,
                WASDControls(),
                100,
                50
            ),
            Player(
                100, 200,
                GREEN,
                ArrowsControls(),
                100,
                50
            )
        ]
        self.blocks: list[Block] = [
            Block(
                600, 300, 50, 50,
            ),
            Block(
                600, 400, 50, 50,
            ),
            Block(
                700, 300, 50, 50,
            ),
            Block(
                700, 400, 50, 50,
            ),
        ]

        self.bullets: list[Bullet] = []

    def run(self):
        while self.running:
            self.clock.tick(self.configs.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill(BLACK)

            keys = pygame.key.get_pressed()
            
            for player in self.players:
                player.reborn(keys)
                if player.is_dead:
                    player.remove(self.screen)
                    continue
                player.take_hits(self.bullets)
                player.move(self.blocks, keys)
                self.bullets.extend(player.shoot(keys))
                player.draw(self.screen)

            for block in self.blocks:
                block.update(self.bullets)
                block.draw(self.screen)

            for index, bullet in enumerate(self.bullets):
                if bullet.remove_ready:
                    self.bullets.pop(index)
                    bullet.remove(self.screen)
                else:
                    bullet.update(self.screen)

            pygame.display.flip()

        pygame.quit()
